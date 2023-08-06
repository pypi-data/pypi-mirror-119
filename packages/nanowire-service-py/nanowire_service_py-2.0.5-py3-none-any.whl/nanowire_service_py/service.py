from typing import Any, Dict, Callable, List
import json, traceback, sys

from pydantic import BaseModel, ValidationError
from dapr.clients import DaprClient
from loguru import logger
from .utils import safe_dump, now, path
from .types import ChildAction, Environment, Task, TaskOutput, PluginOutput


def children_actions(
    task: Task, args: Dict[str, Any], meta: Dict[str, Any] = {}
) -> List[ChildAction]:
    if task.children is None:
        return []
    return [
        ChildAction(
            parent=task.current.id,
            child=c.id,
            plugin=c.plugin,
            args={**c.default_args, **args},
            meta={**c.meta, **meta},
        )
        for c in task.children
    ]


class StageProfiler:
    entries: Dict[str, str]

    def __init__(self):
        self.entries = {}

    def mark(self, tag):
        self.entries[tag] = now()


class ServiceClient:
    env: Environment
    route: str
    failed: str
    finished: str

    def __init__(  # type: ignore
        self,
        env: Any,
        logger=logger,
    ):
        self.client = DaprClient()
        self.raw_env = env
        self.env = Environment(**env)

        self.route = "/receive"
        self.log = logger
        self.failed = "failed"
        self.finished = "finished"

        self.configure()

    def subscriptions(self):
        return [
            {
                "topic": self.env.DAPR_APP_ID,
                "route": self.route,
                "pubsubname": self.env.PUB_SUB,
            }
        ]

    # Any custom behaviour that the service might need
    def configure(self) -> None:
        pass

    def execute(self, task: Any, profiler: StageProfiler) -> TaskOutput:
        raise Exception("Please define execute method")

    def handle_request(self, body):
        uuid = path(["uuid"], body)
        self.log.debug(f"[{uuid}] Task received")
        started = now()
        try:
            task = Task(**body)
            # TODO: if body is an url, should try and retrieve it
            # before passing down for validation
            profiler = StageProfiler()
            plugin_result = self.execute(body, profiler)
            if not isinstance(plugin_result, PluginOutput):
                raise Exception(
                    "Received invalid task output. Expected PluginOutput, received: {}".format(
                        repr(plugin_result)
                    )
                )
            finished = now()
            self.log.debug("[{uuid}] Task finished, publishing", uuid=task.uuid)
            result = TaskOutput(
                uuid=task.uuid,
                started=started,
                finished=finished,
                profiling=profiler.entries,
                output=plugin_result.output,
                actions=plugin_result.actions,
                plugin_id=task.current.id,
            )
            output = result.dict()
            self.publish(self.finished, output)
            self.log.debug("[{uuid}] Published, done", uuid=task.uuid)
        except ValidationError as e:
            exc_info = sys.exc_info()
            exception = "".join(traceback.format_exception(*exc_info))
            self.log.error(f"[{uuid}] Failed to parse task body {exception}")
            output = {
                "uuid": uuid,
                "started": started,
                "finished": now(),
                "error": {
                    "body": body,
                    "why": "ValidationError",
                    "errors": json.loads(e.json()),
                },
            }
            self.publish(self.failed, output)
        except Exception as e:
            exc_info = sys.exc_info()
            exception = "".join(traceback.format_exception(*exc_info))
            self.log.error(f"[{uuid}] Failed to parse task body {exception}")
            output = {
                "uuid": uuid,
                "started": started,
                "finished": now(),
                "error": {
                    "body": body,
                    "why": "Exception",
                    "message": str(e),
                    "type": repr(e),
                    "exception": exception,
                },
            }
            self.publish(self.failed, output)
        return output

    def publish(self, topic: str, data: Dict[str, Any]) -> None:
        self.client.publish_event(
            pubsub_name=self.env.OUTPUT_PUB_SUB,
            topic_name=topic,
            data_content_type="application/json",
            data=safe_dump(data),
        )

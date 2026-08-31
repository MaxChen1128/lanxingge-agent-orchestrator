"""任务规划器。

将高层目标拆解为有序子任务，支撑层级式主管-工人编排拓扑。
"""

from dataclasses import dataclass, field
from typing import List

from .llm_client import ChatMessage, LLMClient


@dataclass
class SubTask:
    """一个子任务。"""

    task_id: str
    description: str
    depends_on: List[str] = field(default_factory=list)


class Planner:
    """基于大语言模型的任务规划器。"""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def decompose(self, goal: str) -> List[SubTask]:
        """将目标拆解为有序子任务列表。"""
        prompt = (
            "你是一个任务规划器。请将以下目标拆解为有序子任务，"
            f"每个子任务一行，格式：子任务描述。\n目标：{goal}"
        )
        resp = self.llm.complete([ChatMessage(role="user", content=prompt)])
        tasks: List[SubTask] = []
        for i, line in enumerate(resp.splitlines()):
            line = line.strip()
            if not line:
                continue
            tasks.append(SubTask(task_id=f"t{i + 1}", description=line))
        if not tasks:
            tasks.append(SubTask(task_id="t1", description=goal))
        return tasks

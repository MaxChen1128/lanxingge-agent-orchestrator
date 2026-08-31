"""智能体（Agent）定义与执行单元。"""

from dataclasses import dataclass, field
from typing import List

from .llm_client import ChatMessage, LLMClient
from .memory import MemoryStore
from .tool import ToolRegistry


@dataclass
class AgentSpec:
    """智能体规格定义。"""

    name: str
    role: str
    system_prompt: str
    tools: List[str] = field(default_factory=list)
    model: str = "default"


class Agent:
    """单个智能体执行单元。"""

    def __init__(self, spec: AgentSpec, llm: LLMClient, registry: ToolRegistry, memory: MemoryStore):
        self.spec = spec
        self.llm = llm
        self.registry = registry
        self.memory = memory

    def act(self, task: str, context: str = "") -> str:
        """基于任务与上下文执行一次推理。"""
        sys_msg = ChatMessage(role="system", content=self.spec.system_prompt)
        tool_hint = "可用工具：" + ", ".join(self.spec.tools) if self.spec.tools else "无可用工具"
        user_msg = ChatMessage(
            role="user",
            content=f"任务：{task}\n上下文：{context}\n{tool_hint}",
        )
        history = self.memory.recent()
        messages = [sys_msg] + history + [user_msg]
        result = self.llm.complete(messages)
        self.memory.add(user_msg)
        self.memory.add(ChatMessage(role="assistant", content=result))
        return result

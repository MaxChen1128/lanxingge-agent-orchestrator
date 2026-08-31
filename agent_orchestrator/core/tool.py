"""工具（Tool）抽象与注册中心。

Agent 可挂载工具以扩展执行能力；注册中心统一管理工具实例与元数据。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ToolResult:
    """工具执行结果。"""

    success: bool
    output: str


class Tool(ABC):
    """工具抽象基类，子类实现具体能力。"""

    name: str = ""
    description: str = ""

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        """执行工具逻辑。"""
        raise NotImplementedError


class ToolRegistry:
    """工具注册中心。"""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> List[dict]:
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

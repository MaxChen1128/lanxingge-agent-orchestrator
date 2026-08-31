"""大语言模型客户端抽象层。

定义统一的对话接口，屏蔽不同模型后端的差异；内置离线演示客户端，
真实部署时仅需实现 ``complete`` 方法即可对接任意网关。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class ChatMessage:
    """一条对话消息。"""

    role: str
    content: str


class LLMClient(ABC):
    """大语言模型客户端抽象基类。"""

    @abstractmethod
    def complete(self, messages: List[ChatMessage], **kwargs) -> str:
        """根据对话历史生成回复。"""
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """离线演示客户端：不调用真实接口，按规则生成响应，便于本地联调。"""

    def __init__(self, echo: bool = False):
        self.echo = echo

    def complete(self, messages: List[ChatMessage], **kwargs) -> str:
        last = messages[-1].content if messages else ""
        if self.echo:
            return f"[演示] 已接收指令：{last[:80]}"
        return f"已完成子任务：{last[:60]}"


class OpenAICompatibleClient(LLMClient):
    """兼容 OpenAI 协议的客户端，可对接自建或第三方模型网关。"""

    def __init__(self, base_url: str, api_key: str, model: str = "default"):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    def complete(self, messages: List[ChatMessage], **kwargs) -> str:
        # 真实部署时在此发起 HTTP 请求；此处保留抽象，避免硬编码第三方依赖。
        raise NotImplementedError("请在部署环境中接入真实 LLM 网关")

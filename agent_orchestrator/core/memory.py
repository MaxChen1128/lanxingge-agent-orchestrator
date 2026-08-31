"""记忆存储。

维护短期对话缓冲与长期键值记忆，为多轮协作与上下文复用提供支撑。
"""

from collections import OrderedDict
from typing import List, Optional

from .llm_client import ChatMessage


class MemoryStore:
    """短期+长期记忆存储。"""

    def __init__(self, short_term_limit: int = 20):
        self._short: List[ChatMessage] = []
        self._long: "OrderedDict[str, str]" = OrderedDict()
        self.short_term_limit = short_term_limit

    def add(self, message: ChatMessage) -> None:
        """追加一条短期记忆。"""
        self._short.append(message)
        if len(self._short) > self.short_term_limit:
            self._short.pop(0)

    def recent(self, k: Optional[int] = None) -> List[ChatMessage]:
        """返回最近 k 条短期记忆。"""
        return self._short[-k:] if k else list(self._short)

    def remember(self, key: str, value: str) -> None:
        """写入长期记忆。"""
        self._long[key] = value

    def recall(self, key: str) -> Optional[str]:
        """读取长期记忆。"""
        return self._long.get(key)

    def clear_short(self) -> None:
        self._short.clear()

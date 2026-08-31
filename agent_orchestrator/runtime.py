"""运行时（Runtime）。

负责任务执行的状态跟踪与异常捕获，为编排过程提供可观测性。
"""

from typing import Callable, Dict

from .utils.logger import get_logger

logger = get_logger("runtime")


class Runtime:
    """轻量执行运行时。"""

    def __init__(self) -> None:
        self._state: Dict[str, object] = {}

    def execute(self, fn: Callable, *args, **kwargs):
        """执行函数并记录状态；异常时记录错误但不吞没。"""
        try:
            logger.info("开始执行任务")
            result = fn(*args, **kwargs)
            self._state["last_status"] = "ok"
            return result
        except Exception as exc:  # noqa: BLE001
            logger.error(f"任务执行失败：{exc}")
            self._state["last_status"] = "error"
            self._state["last_error"] = str(exc)
            raise

    def status(self) -> Dict[str, object]:
        return dict(self._state)

"""揽星阁 AI 智能体编排引擎。

提供多智能体（Agent）的编排与调度能力，支持顺序、并行、层级主管-工人等
拓扑结构，可作为检索增强、推理调度、提示词评测等上层能力的技术底座。
"""

from .orchestrator import Orchestrator
from .runtime import Runtime

__all__ = ["Orchestrator", "Runtime"]
__version__ = "0.1.0"

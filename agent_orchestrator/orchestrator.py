"""编排器（Orchestrator）。

负责智能体的注册与多种协作拓扑的调度：顺序流水线、并行扇出、层级主管-工人。
"""

from typing import List

from .core.agent import Agent, AgentSpec
from .core.llm_client import LLMClient
from .core.memory import MemoryStore
from .core.planner import Planner
from .core.tool import ToolRegistry
from .utils.logger import get_logger

logger = get_logger("orchestrator")


class Orchestrator:
    """多智能体编排器。"""

    def __init__(self, llm: LLMClient, registry: ToolRegistry = None):
        self.llm = llm
        self.registry = registry or ToolRegistry()
        self.memory = MemoryStore()
        self.planner = Planner(llm)
        self._agents: dict = {}

    def register_agent(self, spec: AgentSpec) -> Agent:
        agent = Agent(spec, self.llm, self.registry, self.memory)
        self._agents[spec.name] = agent
        logger.info(f"已注册智能体：{spec.name}")
        return agent

    def get_agent(self, name: str) -> Agent:
        return self._agents.get(name)

    def run_sequential(self, goal: str, agent_names: List[str]) -> str:
        """顺序流水线：上游结果作为下游上下文。"""
        context = ""
        for name in agent_names:
            agent = self._agents[name]
            logger.info(f"顺序执行智能体：{name}")
            context = agent.act(goal, context)
        return context

    def run_parallel(self, goal: str, agent_names: List[str]) -> List[str]:
        """并行扇出：各智能体独立处理同一目标。"""
        results = []
        for name in agent_names:
            agent = self._agents[name]
            logger.info(f"并行执行智能体：{name}")
            results.append(agent.act(goal, ""))
        return results

    def run_hierarchical(self, goal: str, supervisor: str, workers: List[str]) -> str:
        """层级主管-工人：主管拆解任务，工人执行后由主管汇总。"""
        sup = self._agents[supervisor]
        plan = self.planner.decompose(goal)
        logger.info(f"主管 {supervisor} 拆解得到 {len(plan)} 个子任务")
        summary = []
        for subtask in plan:
            worker = self._agents[workers[0]] if workers else sup
            summary.append(worker.act(subtask.description, ""))
        return sup.act("汇总以下结果：\n" + "\n".join(summary), "")

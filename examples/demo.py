"""演示：使用离线 Mock 客户端跑通顺序编排。"""

from agent_orchestrator import Orchestrator
from agent_orchestrator.core.agent import AgentSpec
from agent_orchestrator.core.llm_client import MockLLMClient


def main():
    orch = Orchestrator(llm=MockLLMClient(echo=True))
    orch.register_agent(AgentSpec(
        name="planner_agent",
        role="任务规划",
        system_prompt="你是任务规划专家，负责拆解目标。",
    ))
    orch.register_agent(AgentSpec(
        name="executor_agent",
        role="任务执行",
        system_prompt="你是任务执行专家，负责落地方案。",
    ))

    result = orch.run_sequential(
        "为电商客服搭建智能体",
        ["planner_agent", "executor_agent"],
    )
    print("最终结果：", result)


if __name__ == "__main__":
    main()

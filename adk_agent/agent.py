from google.adk.agents import SequentialAgent
from google.adk.agents import ParallelAgent

from adk_agent.subagents.parsing import parsing_agent
from adk_agent.subagents.preprocess import preprocess_agent
from adk_agent.subagents.risk import risk_agent
from adk_agent.subagents.summary import summary_agent

parse_pipeline = SequentialAgent(
    name="ParsingPipelineAgent",
    sub_agents=[parsing_agent, preprocess_agent],
    description="Executes a sequence of parsing and preprocessing on legal documents.",
)

flow_pipeline = ParallelAgent(
    name = "RootAgent",
    sub_agents = [risk_agent, summary_agent],
    description="Creates a summary and risk analyser",
)

root_agent = SequentialAgent(
    name="RootSequentialAgent",
    sub_agents=[parse_pipeline, flow_pipeline],
    description="Executes the full pipeline from parsing to risk analysis and summary.",
)
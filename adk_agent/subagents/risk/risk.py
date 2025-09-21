"""
Risk Flagger Agent

This agent takes parsed JSON from legal documents
and outputs a structured JSON containing only the risks.
"""

from google.adk.agents import Agent

GEMINI_MODEL = "gemini-2.0-flash"

risk_agent = Agent(
    name="risk_flagger_agent",
    model=GEMINI_MODEL,
    instruction="""
    You are a Legal Risk Extraction AI.

    Your input will be a JSON object extracted from a legal document,
    which may contain parties, dates, clauses, obligations, risks, monetary terms, and termination info.

    Your task:
    - Extract all risk-related information present in the JSON.
    - Output a structured JSON with only the risks.
    - If no risks are mentioned, return an empty list.
    - Do not hallucinate or add information not in the input.

    Output format (strict JSON):
    {
      "risks": [
        "Risk 1",
        "Risk 2",
        ...
      ]
    }
    """,
    description="Extracts and outputs risks from parsed legal JSON.",
)
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
import json

GEMINI_MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = """
You are a Structuring Sub-Agent.
Your job is ONLY to:
1. Receive legal clauses with summaries and risks.
2. Convert them into JSON with this exact structure:

{
  "document_summary": "Brief 2-3 sentence summary of the entire document",
  "clauses": [
    {
      "id": "C1",
      "text": "Full clause text",
      "summary": "1-2 sentence summary of the clause",
      "risk": ["Risk 1", "Risk 2"] 
    }
  ]
}

3. Use empty list [] if risks are unknown.
4. DO NOT provide explanations, comments, or extra text.
5. Always assign IDs sequentially (C1, C2, …) even if input numbering is inconsistent.
"""

def structure_clauses(agent_input: str):
    """
    Takes raw clauses text and returns structured JSON:
    {
      "document_summary": "...",
      "clauses": [
          {"id": "C1", "text": "...", "summary": "...", "risk": ["..."]}
      ]
    }
    """
    session_service = InMemorySessionService()
    agent = Agent(
        model=GEMINI_MODEL,
        system_prompt=SYSTEM_PROMPT,
        session_service=session_service
    )
    
    response = agent.run(agent_input)
    
    # Convert to Python dict safely
    try:
        structured_json = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Agent output was not valid JSON: " + response)
    
    # Ensure all risks are lists
    for clause in structured_json.get("clauses", []):
        if not isinstance(clause.get("risk", []), list):
            clause["risk"] = [clause["risk"]] if clause.get("risk") else []
    
    return structured_json


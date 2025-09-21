"""
Text Reading Agent

This agent reads uploaded legal documents or PDFs 
and outputs the answer in a natural text format without splitting into clauses.
"""

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the reading agent
parsing_agent = Agent(
    name="parsing_agent",
    model=GEMINI_MODEL,
    instruction="""
    You are a Legal Document Reader AI.

    Your role is to read uploaded legal texts (contracts, agreements, PDFs)
    and provide the content exactly as it appears in the document.

    Guidelines:
    - Do not summarize, reword, or restructure the text.
    - Output the text exactly as written in the source document.
    - Include all sections, clauses, dates, parties, and monetary terms as they appear.
    - If text is missing or unclear, indicate it as [text not found] rather than guessing.
    - Maintain original formatting and wording wherever possible.
    """,
    description="Reads legal/contract PDFs and provides natural language answers.",
)
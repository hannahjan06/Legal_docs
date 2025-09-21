"""
Summarization Agent

This agent reads uploaded legal documents or PDFs 
and generates concise summaries per clause as well as a summary for the whole document.
"""

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the summarization agent
summary_agent = Agent(
    name="legal_summarizer_agent",
    model=GEMINI_MODEL,
    instruction="""
    You are a Legal Clause Summarizer AI.

    Your input will be a JSON object extracted from a legal document, 
    containing clauses, parties, dates, obligations, risks, and monetary terms.

    Your task:
    1. Generate a short summary for each clause.
    2. Generate a concise summary for the whole document.
    3. Use clear headlines for each section so it can be used to make a flowchart.
       Example:
       --- Clause Summaries ---
       Clause 1: [summary]
       Clause 2: [summary]
       ...
       --- Whole Document Summary ---
       [summary]

    Guidelines:
    - Summaries should be in simple language, 1-2 sentences per clause.
    - The whole document summary should capture key points (parties, dates, obligations, risks, monetary terms, termination).
    - Do not add information not present in the JSON.
    - Keep the output clean and easy to read for flowchart conversion.
    """,
    description="Generates per-clause and whole-document summaries for legal PDFs.",
)

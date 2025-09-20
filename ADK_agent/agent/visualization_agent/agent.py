import json
import uuid
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService

GEMINI_MODEL = "gemini-2.0-flash"

# --- Utility function to generate unique node IDs ---
def generate_node_id():
    return str(uuid.uuid4())[:8]

# --- Function to convert structured JSON to flowchart JSON ---
def create_visual_json(input_json):
    visual_json = {"nodes": [], "edges": []}

    # --- Add summary node ---
    summary_id = generate_node_id()
    visual_json["nodes"].append({
        "id": summary_id,
        "label": input_json.get("document_summary", "Document Summary"),
        "type": "summary",
        "color": "lightblue",
        "shape": "box"
    })

    # --- Add clause nodes with risk-based colors ---
    clause_ids = {}
    for clause in input_json.get("clauses", []):
        node_id = generate_node_id()
        clause_ids[clause["clause_id"]] = node_id

        risk_text = clause.get("risk", "").lower()
        if "high" in risk_text:
            color = "red"
        elif "medium" in risk_text:
            color = "orange"
        else:
            color = "green"

        visual_json["nodes"].append({
            "id": node_id,
            "label": f'{clause["clause_id"]}: {clause.get("summary", "")}',
            "type": "clause",
            "color": color,
            "shape": "ellipse",
            "tooltip": f"Summary: {clause.get('summary','')}\nRisk: {clause.get('risk','')}"
        })

    # --- Connect summary node to the first clause ---
    sorted_clauses = input_json.get("clauses", [])
    if sorted_clauses:
        first_clause_id = clause_ids[sorted_clauses[0]["clause_id"]]
        visual_json["edges"].append({
            "from": summary_id,
            "to": first_clause_id,
            "relationship": "summary_of"
        })

    # --- Add sequential edges between clauses ---
    for i in range(len(sorted_clauses)-1):
        visual_json["edges"].append({
            "from": clause_ids[sorted_clauses[i]["clause_id"]],
            "to": clause_ids[sorted_clauses[i+1]["clause_id"]],
            "relationship": "follows"
        })

    return visual_json

# --- Visualization Sub-Agent ---
visualization_agent = Agent(
    name="visualization_agent",
    model=GEMINI_MODEL,
    instruction="""
    You are a sub-agent that receives structured clause JSON and produces
    a flowchart-ready JSON with nodes and edges. Do NOT chat or explain.
    """,
    description="Generates flowchart JSON from structured clauses.",
    session_service=InMemorySessionService(),
    on_message=create_visual_json
)

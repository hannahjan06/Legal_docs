from google.adk.agents import Agent

# Root agent defined directly here to avoid circular imports
root_agent = Agent(
    name="flowchart_generator_agent",
    model="gemini-2.0-flash",
)

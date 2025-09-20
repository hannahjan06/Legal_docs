import asyncio
from greeting_agent.agent import agent as greeting
from structuring_agent.agent import agent as structuring
from flowchart_generator_agent.agent import agent as flowchart

async def main():
    # 1️⃣ Test greeting agent
    greeting_resp = await greeting.ask("Hello, how are you?")
    print("Greeting Agent Response:")
    print(greeting_resp.text)
    print("-" * 50)

    # 2️⃣ Test structuring agent
    structuring_input = "Summarize this clause: 'The tenant must pay rent before the 5th of each month.'"
    structuring_resp = await structuring.ask(structuring_input)
    print("Structuring Agent Response:")
    print(structuring_resp.text)
    print("-" * 50)

    # 3️⃣ Test flowchart generator agent
    flowchart_input = "Convert this structured JSON to a flowchart-ready format: {'clauses':[{'id':1,'text':'Pay rent'}]}"
    flowchart_resp = await flowchart.ask(flowchart_input)
    print("Flowchart Agent Response:")
    print(flowchart_resp.text)
    print("-" * 50)

# Run the async main
asyncio.run(main())

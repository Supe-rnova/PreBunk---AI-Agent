"""Step 2 check #2: talk to the running MCP server exactly like the agent will."""
import asyncio

from fastmcp import Client

MESSAGE = "Share this before they delete it! They don't want you to know the truth about the water supply."


async def main():
    async with Client("http://127.0.0.1:8001/mcp") as client:
        tools = await client.list_tools()
        print("Tools on the server:", [t.name for t in tools])

        result = await client.call_tool("retrieve_techniques", {"text": MESSAGE})
        print("\nretrieve_techniques ->")
        for match in result.data:
            print("  ", match)


asyncio.run(main())

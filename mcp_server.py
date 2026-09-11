"""Prebunk MCP server: exposes the agent's tools over MCP (HTTP, port 8001).

Step 2 adds retrieve_techniques. Step 3 adds fact_check to this same server.
Run with:  uv run mcp_server.py
"""
from fastmcp import FastMCP

import retrieval

mcp = FastMCP("prebunk-tools")


@mcp.tool
def retrieve_techniques(text: str, k: int = 3) -> list[dict]:
    """Find the cognitive biases and manipulation techniques (fear appeals, false urgency,
    scapegoating, conspiracy framing, etc.) that a message most resembles, retrieved from a
    curated knowledge base. Use this for any message that may be trying to persuade,
    frighten, or provoke the reader. Returns [{id, name, definition, score}], where score
    is 0-1 similarity; an empty list means no technique matched closely enough."""
    k = max(1, min(int(k), 5))
    return retrieval.retrieve_techniques(text, k=k)


if __name__ == "__main__":
    retrieval.get_collection()  # build or load the vector index before accepting requests
    mcp.run(transport="http", host="127.0.0.1", port=8001)

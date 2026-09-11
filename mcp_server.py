"""Prebunk MCP server: exposes the agent's tools over MCP (HTTP, port 8001).

Tools: retrieve_techniques (Step 2) and fact_check (Step 3).
Run with:  uv run mcp_server.py
"""
from fastmcp import FastMCP

import retrieval
from fact_check import fact_check as run_fact_check

mcp = FastMCP("prebunk-tools")


@mcp.tool
def retrieve_techniques(text: str, k: int = 3) -> list[dict]:
    """Find the cognitive biases and manipulation techniques (fear appeals, false urgency,
    scapegoating, conspiracy framing, etc.) that a message most resembles, retrieved from a
    curated knowledge base. Use this for any message that may be trying to persuade,
    frighten, or provoke the reader. Returns [{id, name, definition, score, matched_markers}]:
    score is 0-1 (semantic similarity plus a boost for tell-tale phrases); matched_markers
    lists the exact phrases found in the message. An empty list means no technique matched closely enough."""
    k = max(1, min(int(k), 5))
    return retrieval.retrieve_techniques(text, k=k)


@mcp.tool
def fact_check(text: str) -> dict:
    """Check the main factual claim in a message against Wikipedia (best effort, single source).
    Use this when the message states something checkable: a statistic, an event, a health or
    science claim, or an official announcement. Skip it for pure opinion or emotional content.
    Returns {claim, verdict, source_url, source_title, evidence}; verdict is "true", "false"
    or "unverified". "unverified" means Wikipedia did not clearly settle it - NOT that the
    claim is true."""
    return run_fact_check(text)


if __name__ == "__main__":
    retrieval.get_collection()  # build or load the vector index before accepting requests
    mcp.run(transport="http", host="127.0.0.1", port=8001)

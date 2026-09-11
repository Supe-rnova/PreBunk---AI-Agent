"""Accuracy eval for technique retrieval on the full gold set. Uses ZERO Gemini calls
(retrieval runs locally), so it doesn't touch your free-tier quota.
The MCP server must be running. Saves eval_retrieval_results.md."""
import asyncio

from fastmcp import Client

from eval_set import EVAL_SET


async def main():
    rows, passed, total = [], 0, 0
    async with Client("http://127.0.0.1:8001/mcp") as client:
        for case in EVAL_SET:
            if case.get("techniques") is None:
                continue  # this message only tests fact-checking or escalation
            result = await client.call_tool("retrieve_techniques", {"text": case["text"]})
            got = result.data or []
            got_ids = [m["id"] for m in got]
            if case["techniques"]:
                check, ok = "technique found", any(i in got_ids for i in case["techniques"])
            else:
                check, ok = "no false alarm", not got_ids
            passed, total = passed + ok, total + 1
            shown = ", ".join(f"{m['name']} ({m['score']:.2f})" for m in got) or "none"
            print(f"{case['id']} {'PASS' if ok else 'FAIL'}  {check:15}  expected {case['techniques'] or 'nothing'}  got: {shown}")
            rows.append(f"| {case['id']} | {case['note']} | {', '.join(case['techniques']) or 'nothing'} | {shown} | {'PASS' if ok else 'FAIL'} |")

    report = ["# Technique retrieval accuracy (no LLM involved)", "",
              f"**{passed}/{total} passed**", "",
              "| ID | Message type | Expected | Retrieved (score) | Result |", "|---|---|---|---|---|"] + rows
    with open("eval_retrieval_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print(f"\n{passed}/{total} passed. Saved eval_retrieval_results.md")


asyncio.run(main())

"""Step 4 check: run the full agent on three messages. The MCP server must be running."""
import asyncio
import json

from langfuse import get_client

from agent import analyze_message

SAMPLES = [
    "Studies show [group] commits far more crime than everyone else - we need to stop letting them in before it's too late.",
    "WARNING!!! Forward to all groups before they delete this: drinking hot water every hour kills the new virus. Doctors don't want you to know.",
    "Hi all, the society water tank cleaning is on Sunday 10am, so there will be no water supply from 10 to 1.",
]


async def main():
    for text in SAMPLES:
        print("=" * 80)
        print("MESSAGE:", text)
        result = await analyze_message(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    get_client().flush()  # make sure all traces reach Langfuse before the script exits
    print("\nDone - open Langfuse -> Tracing to see one trace per message.")


asyncio.run(main())

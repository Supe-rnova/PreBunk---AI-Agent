"""Step 2 check #1: raw retrieval scores. Run BEFORE starting the MCP server."""
from retrieval import retrieve_techniques, MIN_SCORE

SAMPLES = [
    # should match something
    "Studies show [group] commits far more crime than everyone else - we need to stop letting them in before it's too late.",
    "FORWARD TO ALL GROUPS!!! Government will delete this video tonight. Doctors don't want you to know onion juice cures diabetes.",
    "Message from RBI: all 500 rupee notes will be invalid from Monday. Forwarded as received.",
    "We've already spent two years on this project, so we can't stop now.",
    # should match nothing (or only weakly)
    "The library will be closed on Monday for the public holiday and reopens Tuesday at 9am.",
    "Reminder: team lunch is at 1pm on Friday, please let me know if you have dietary requirements.",
]

print(f"Current MIN_SCORE = {MIN_SCORE}  (showing top 3 with NO threshold)\n")
for text in SAMPLES:
    print(text[:90])
    for m in retrieve_techniques(text, k=3, min_score=0.0):
        flag = "PASS " if m["score"] >= MIN_SCORE else "below"
        extra = f"   markers: {m['matched_markers']}" if m["matched_markers"] else ""
        print(f"   {m['score']:.2f} [{flag}] {m['name']}{extra}")
    print()

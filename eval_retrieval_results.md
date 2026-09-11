# Technique retrieval accuracy (no LLM involved)

**9/11 passed**

| ID | Message type | Expected | Retrieved (score) | Result |
|---|---|---|---|---|
| G01 | health misinformation + conspiracy | M07, M05 | none | FAIL |
| G02 | scapegoating, hostility toward a group | M03 | Scapegoating (us vs. them) (0.66), Anecdote as proof (cherry-picking) (0.53), Fear appeal (0.41) | PASS |
| G03 | anecdote as proof, health | M09 | none | FAIL |
| G05 | false urgency | M02, M06 | False urgency (0.55) | PASS |
| G06 | false dichotomy | M04, M08, M10 | False dichotomy (0.41) | PASS |
| G07 | discrediting | M10, M07 | Discrediting (ad hominem) (0.42), Conspiracy framing (0.42) | PASS |
| G08 | impersonation + urgency | M06, M02 | False urgency (0.54) | PASS |
| G11 | greeting | nothing | none | PASS |
| G12 | hard negative: contains 'deadline' | nothing | none | PASS |
| G13 | announcement | nothing | none | PASS |
| G14 | hard negative: statistic with a named source | nothing | none | PASS |

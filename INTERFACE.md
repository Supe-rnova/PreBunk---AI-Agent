# Interfaces between the pieces (as built)

Rule for every step: **if something comes back empty, fails, or is unclear, treat it as "not confident", never as "fine".**

## 1. Telegram bot -> Agent
`analyze_message(text: str) -> {"reply": str, "escalate": bool, "escalation_note": str}` (async)

- The bot always sends `reply` to the user.
- If `escalate` is true, it also sends the original message, the reply and `escalation_note` to `REVIEWER_CHAT_ID`.
- Messages with no text (for example a sticker): the bot replies "I can only check text messages right now". Photo captions are analysed.

## 2. Agent -> MCP tool `retrieve_techniques(text, k=3)`
Returns `[{"id", "name", "definition", "score", "matched_markers"}]`, or `[]` if nothing reaches 0.40.
Score = best cosine similarity over the technique's chunks + 0.20 per marker phrase found (at most 2).

## 3. Agent -> MCP tool `fact_check(text)`
Returns `{"claim", "verdict": "true" | "false" | "unverified", "source_url", "source_title", "evidence"}`. Every field is always present.
`"unverified"` covers: no checkable claim, nothing found on Wikipedia, excerpts don't address the claim, or the check failed (then `evidence` says "did not run").

## 4. Draft -> Critic -> Rule checks -> Router
- Critic returns `{"confidence": 0-1, "well_supported": bool, "risk": "low" | "medium" | "high", "issues": [...]}`. If it fails, it counts as confidence 0, unsupported, high risk.
- Rule checks: a link not found in the evidence makes the draft unsupported; if any tool failed, confidence is capped at 0.6.
- Router:
  - `confidence >= 0.7` and `well_supported` and not (high risk with the claim unresolved) -> send as-is.
  - Otherwise -> softened reply, `escalate = true`, with a reason.

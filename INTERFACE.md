# The four handoffs — decided, so nobody has to guess

One example message runs through all four gates below, so you can see exactly
what's happening at each step instead of reading abstract rules.

**Example message someone forwards to the bot:**
> "Studies show [group] commits far more crime than everyone else — we need to
> stop letting them in before it's too late."

Rule for every gate, when in doubt: **if something comes back empty or unclear,
treat it as "not confident" rather than guessing.** That one rule covers most
of the edge cases below without anyone having to think hard about them.

---

## Gate 1 — Telegram bot → Agent

**What crosses this line:** just the plain text of the forwarded message.
Nothing fancier — no sender info, no timestamps. Keep it to one thing: a
string of text.

```
IN:  "Studies show [group] commits far more crime than everyone else —
      we need to stop letting them in before it's too late."

OUT: a plain text reply, ready to send back as-is
```

**Empty case:** if someone forwards a photo or sticker with no text, the bot
just replies: *"I can only check text messages right now — try forwarding one
with words in it."* No further processing needed.

---

## Gate 2 — Agent → Technique-lookup tool → Agent

**What goes in:** the whole message text (don't bother splitting it into
separate claims — that's a nice-to-have, not needed for tomorrow).

**What comes back:** a list of matches. Each match is three things: a name,
a definition, and a score from 0 to 1 (how well it matches — 1 means a
strong match, 0 means barely related).

```
IN:  "Studies show [group] commits far more crime than everyone else —
      we need to stop letting them in before it's too late."

OUT: [
  { "name": "In-group bias",     "definition": "...", "score": 0.82 },
  { "name": "Base rate neglect", "definition": "...", "score": 0.61 }
]
```

**Empty case:** if nothing scores above roughly 0.5, just return an empty
list `[]`. The agent will later say "no clear technique detected" — that's a
perfectly fine, honest answer.

---

## Gate 3 — Agent → Fact-check tool → Agent

**What goes in:** the whole message text again (same simple rule as Gate 2 —
let the tool figure out if there's a checkable claim in there).

**What comes back:** one result with exactly three fields — the claim it
checked, a verdict that's always one of three words (`"true"`, `"false"`, or
`"unverified"` — never a percentage, never a paragraph), and a source link if
it has one.

```
IN:  "Studies show [group] commits far more crime than everyone else —
      we need to stop letting them in before it's too late."

OUT: {
  "claim": "studies show [group] commits far more crime",
  "verdict": "unverified",
  "source_url": ""
}
```

**Empty case:** no matching fact-check found → verdict is `"unverified"`,
`source_url` is just an empty string `""`. Never leave a field out entirely —
always send all three, even if some are blank. That way whoever writes the
code reading this never has to check "does this field exist?" — only "is it
blank?"

---

## Gate 4 — Draft → Confidence critic → Router → Final reply

**What goes into the critic:** the draft explanation the agent wrote, plus
whatever it got back from Gates 2 and 3.

**What the critic hands back:** exactly two things — a confidence number
(0 to 1) and a yes/no on whether the draft is actually well-supported by the
evidence it was given.

```
OUT: { "confidence": 0.78, "well_supported": true }
```

**The router's decision rule** (this is the whole "guardrail" in one
sentence): confidence 0.7 or higher AND well_supported is true → send the
explanation as-is. Anything else → send it with softer wording, e.g.
*"This might be worth double-checking — I'm not fully certain."*

**Empty case:** if the critic call fails or returns nothing at all, treat it
exactly like low confidence. Never treat "the check didn't run" the same as
"the check passed."

---

## Why bother writing this down

Whoever builds the Telegram bot (Gate 1) can build and test it completely
using fake, made-up versions of Gates 2–4's outputs — they don't need to wait
for the retrieval or fact-check people to finish anything. Same for everyone
else. Nobody's blocked, and when you plug the real pieces in at the end,
they fit, because everyone built to the same shapes from the start.

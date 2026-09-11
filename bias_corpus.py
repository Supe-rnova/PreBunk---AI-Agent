"""Starter corpus for the Cognitive Bias Detector — mirrors corpus.py's SESSIONS
format from the bootcamp repo so it drops into 00_embedding_model.py /
01_vector_db_lab.py / 04_full_pipeline.py with minimal changes.

Each entry's "text" field is what gets embedded — it concatenates the name,
definition, and example so a retrieval query (a claim from the user's text)
matches on meaning, not just keyword overlap.

THIS IS A STARTER SET, NOT A FINISHED ONE. You know this material better than
a generic list does — before tomorrow, go through each entry and:
  1. Tighten any definition that doesn't match how your coursework defines it.
  2. Add 1-2 more examples per bias, ideally ones that sound like real writing
     (a decision memo, a forum post, an essay) rather than a textbook sentence.
  3. Add or correct "markers" — words/phrases a lightweight keyword-scan tool
     could realistically catch before the LLM even looks at the text.
  4. Add any bias from your own program that isn't in this list yet.

EVAL_EXAMPLES at the bottom is a starter gold set: passages with a known
expected label. Expand this tonight too — it's exactly the "small gold set
scored for accuracy + safety before demo" the judging rubric asks for, and
it's much faster to build well now than at 8am tomorrow.
"""

BIASES = [
    {"id": "B01", "name": "Confirmation bias",
     "definition": "The tendency to search for, interpret, and recall information in a way that confirms one's prior beliefs, while giving disproportionately less consideration to alternative possibilities.",
     "example": "I knew the new hire wouldn't work out, and sure enough every mistake she made proved me right — I didn't really notice the things she did well.",
     "markers": ["proves i was right", "as i expected", "just as i thought", "confirms my", "i knew it"],
     "text": "Confirmation bias: the tendency to search for, interpret, and recall information in a way that confirms one's prior beliefs, while giving disproportionately less consideration to alternative possibilities. Example: I knew the new hire wouldn't work out, and sure enough every mistake she made proved me right."},

    {"id": "B02", "name": "Anchoring bias",
     "definition": "Relying too heavily on the first piece of information offered (the 'anchor') when making decisions, even when it is irrelevant to the decision at hand.",
     "example": "The first quote we got was $50,000, so when the second contractor quoted $38,000 it felt like a steal — even though we never checked if $38,000 was actually reasonable.",
     "markers": ["initial estimate", "first offer", "starting point of", "compared to the original"],
     "text": "Anchoring bias: relying too heavily on the first piece of information offered when making decisions, even when it is irrelevant. Example: the first quote we got was $50,000, so the second quote of $38,000 felt like a steal even though we never checked if it was reasonable."},

    {"id": "B03", "name": "Availability heuristic",
     "definition": "Overestimating the likelihood of events based on how easily examples come to mind, often because of recent or vivid media coverage, rather than actual statistical frequency.",
     "example": "After seeing three plane-crash stories this month, she decided flying was too dangerous and booked a 14-hour drive instead.",
     "markers": ["i keep hearing about", "seems to happen all the time", "just saw a story about", "everyone's talking about"],
     "text": "Availability heuristic: overestimating the likelihood of events based on how easily examples come to mind rather than actual statistical frequency. Example: after seeing three plane-crash stories this month, she decided flying was too dangerous."},

    {"id": "B04", "name": "Sunk cost fallacy",
     "definition": "Continuing a behavior or endeavor as a result of previously invested resources (time, money, effort), even when abandoning it would be more rational.",
     "example": "We've already spent eight months on this feature, so we can't cancel it now, even though nobody wants it anymore.",
     "markers": ["already invested", "we've come this far", "too much time to quit now", "can't waste what we've put in"],
     "text": "Sunk cost fallacy: continuing a behavior because of previously invested resources, even when stopping would be more rational. Example: we've already spent eight months on this feature so we can't cancel it now, even though nobody wants it anymore."},

    {"id": "B05", "name": "Framing effect",
     "definition": "Drawing different conclusions from the same information depending on how it is presented — for example, as a potential gain versus a potential loss.",
     "example": "The surgery has a '90% survival rate' sounded reassuring, but the same procedure described as having a '10% mortality rate' made the patient hesitant, even though the numbers are identical.",
     "markers": ["sounds better when you say", "depends how you phrase it", "put positively", "put negatively"],
     "text": "Framing effect: drawing different conclusions from the same information depending on how it is presented, e.g. as a gain versus a loss. Example: a '90% survival rate' sounds reassuring while the same procedure's '10% mortality rate' sounds alarming, even though the numbers are identical."},

    {"id": "B06", "name": "Hindsight bias",
     "definition": "The tendency, after an event has occurred, to see it as having been predictable, despite there having been little or no objective basis for predicting it beforehand.",
     "example": "After the startup failed, the board said 'we always knew the market wasn't ready' — despite having approved the funding themselves a year earlier.",
     "markers": ["i knew it all along", "it was obvious this would happen", "we always knew", "should have seen it coming"],
     "text": "Hindsight bias: the tendency, after an event has occurred, to see it as having been predictable, despite little objective basis for predicting it beforehand. Example: after the startup failed, the board said 'we always knew the market wasn't ready' despite approving the funding a year earlier."},

    {"id": "B07", "name": "Overconfidence bias",
     "definition": "Having excessive confidence in one's own answers, abilities, or judgments relative to their actual accuracy.",
     "example": "I'm 100% sure this migration will go smoothly — I've done dozens of these before, so there's really no need for a rollback plan.",
     "markers": ["100% sure", "definitely will work", "no doubt about it", "there's no need to double check"],
     "text": "Overconfidence bias: having excessive confidence in one's own answers, abilities, or judgments relative to their actual accuracy. Example: I'm 100% sure this migration will go smoothly, so there's no need for a rollback plan."},

    {"id": "B08", "name": "Bandwagon effect",
     "definition": "Adopting a belief or behavior primarily because many other people have already adopted it, rather than because of independent evaluation of the evidence.",
     "example": "Everyone on the team already picked this framework, so I didn't bother comparing it to the alternatives before agreeing.",
     "markers": ["everyone is doing it", "most people agree", "the whole team already", "since everyone else"],
     "text": "Bandwagon effect: adopting a belief or behavior primarily because many other people have already adopted it, rather than independent evaluation. Example: everyone on the team already picked this framework, so I didn't compare it to alternatives."},

    {"id": "B09", "name": "Status quo bias",
     "definition": "A preference for the current state of affairs, where any change from the baseline is perceived as a loss, leading to resistance to change even when change would be beneficial.",
     "example": "We know the current process is slow, but we've always done it this way, so let's not risk changing it before the deadline.",
     "markers": ["we've always done it this way", "why fix what isn't broken", "let's not rock the boat", "stick with what we know"],
     "text": "Status quo bias: a preference for the current state of affairs, where change is perceived as a loss even when it would be beneficial. Example: we know the current process is slow, but we've always done it this way, so let's not change it."},

    {"id": "B10", "name": "Self-serving bias",
     "definition": "Attributing successes to one's own abilities and efforts, while attributing failures to external factors outside one's control.",
     "example": "When sales were up, the manager credited her strategy; when sales fell, she blamed the economy.",
     "markers": ["wasn't my fault", "out of my control", "credit goes to my", "circumstances beyond our control"],
     "text": "Self-serving bias: attributing successes to one's own abilities and efforts while attributing failures to external factors. Example: when sales were up the manager credited her strategy; when sales fell she blamed the economy."},

    {"id": "B11", "name": "Halo effect",
     "definition": "Letting a positive impression of a person, brand, or product in one area influence opinion or feelings about them in unrelated areas.",
     "example": "He's such a brilliant engineer, so I'm sure his advice on hiring will be great too.",
     "markers": ["since they're so good at", "he's brilliant so", "such a great company, so their"],
     "text": "Halo effect: letting a positive impression in one area influence opinion in unrelated areas. Example: he's such a brilliant engineer, so I'm sure his advice on hiring will be great too."},

    {"id": "B12", "name": "Negativity bias",
     "definition": "Giving greater psychological weight to negative experiences or information than to positive or neutral experiences of equal magnitude.",
     "example": "The performance review had nine positive comments and one criticism — but the employee could only think about the criticism for days.",
     "markers": ["all i can think about is the one", "the one bad thing", "outweighs everything positive"],
     "text": "Negativity bias: giving greater psychological weight to negative information than to positive or neutral information of equal magnitude. Example: a review had nine positive comments and one criticism, but the employee could only think about the criticism."},

    {"id": "B13", "name": "Optimism bias",
     "definition": "Overestimating the likelihood of positive outcomes and underestimating the likelihood of negative outcomes happening to oneself.",
     "example": "I never buy travel insurance — bad things like that happen to other people, not me.",
     "markers": ["that won't happen to me", "i'll be fine", "it always works out for me"],
     "text": "Optimism bias: overestimating the likelihood of positive outcomes and underestimating negative outcomes happening to oneself. Example: I never buy travel insurance, bad things like that happen to other people, not me."},

    {"id": "B14", "name": "Survivorship bias",
     "definition": "Concentrating on examples that 'survived' a selection process while overlooking those that did not, leading to skewed conclusions.",
     "example": "Every successful founder I read about dropped out of college, so maybe I should drop out too — ignoring the many who dropped out and failed.",
     "markers": ["look at all the successful people who", "the ones who made it", "just look at [name] and [name]"],
     "text": "Survivorship bias: concentrating on examples that survived a selection process while overlooking those that did not. Example: every successful founder I read about dropped out of college, ignoring the many who dropped out and failed."},

    {"id": "B15", "name": "Base rate neglect",
     "definition": "Ignoring general statistical information (the base rate) in favor of specific, often vivid, information about an individual case.",
     "example": "The test is 95% accurate, so if it comes back positive I must have the disease — even though the disease itself is extremely rare in the population.",
     "markers": ["the test says", "must be true because the result showed", "ignoring how rare"],
     "text": "Base rate neglect: ignoring general statistical information in favor of specific, vivid information about an individual case. Example: a test is 95% accurate, so a positive result feels certain even when the underlying disease is extremely rare."},

    {"id": "B16", "name": "Groupthink",
     "definition": "A pattern of thought within a cohesive group where the desire for harmony or conformity results in an irrational or dysfunctional decision-making outcome, and dissent is suppressed.",
     "example": "Nobody raised concerns about the plan in the meeting, because everyone assumed if it were a bad idea, someone else would have already said something.",
     "markers": ["didn't want to be the one to disagree", "went along with it", "no one objected so"],
     "text": "Groupthink: a pattern of thought within a cohesive group where the desire for harmony results in a dysfunctional decision outcome and dissent is suppressed. Example: nobody raised concerns in the meeting because everyone assumed someone else would have."},

    {"id": "B17", "name": "Recency bias",
     "definition": "Giving disproportionate weight to the most recent information or events when making judgments, at the expense of earlier, potentially more representative, data.",
     "example": "He performed well all year, but after one bad week the manager rated him poorly on the annual review.",
     "markers": ["just last week", "most recently", "lately he's been", "based on the last"],
     "text": "Recency bias: giving disproportionate weight to the most recent information at the expense of earlier, more representative data. Example: he performed well all year, but after one bad week the manager rated him poorly on the annual review."},

    {"id": "B18", "name": "Dunning-Kruger effect",
     "definition": "A cognitive bias in which people with low ability or knowledge in a domain overestimate their own competence, while high performers may underestimate theirs.",
     "example": "After one weekend course, he felt qualified to redesign the entire system architecture from scratch.",
     "markers": ["after just one course", "how hard can it be", "i've basically mastered this already"],
     "text": "Dunning-Kruger effect: people with low ability or knowledge in a domain overestimate their own competence. Example: after one weekend course, he felt qualified to redesign the entire system architecture from scratch."},

    {"id": "B19", "name": "Loss aversion",
     "definition": "The tendency to prefer avoiding losses over acquiring equivalent gains — psychologically, losses are felt roughly twice as strongly as gains of the same size.",
     "example": "She refused to sell the stock even at a loss, holding on far longer than made sense, just to avoid 'locking in' the loss.",
     "markers": ["don't want to lock in the loss", "afraid of losing what we have", "rather not risk losing"],
     "text": "Loss aversion: the tendency to prefer avoiding losses over acquiring equivalent gains, since losses are felt more strongly than gains of the same size. Example: she refused to sell the stock even at a loss, holding on far longer than made sense."},

    {"id": "B20", "name": "In-group bias",
     "definition": "The tendency to favor members of one's own group over members of an out-group, in evaluation, resource allocation, or trust, often without a rational basis.",
     "example": "Two candidates gave identical answers, but the interviewer rated the one from her own university as noticeably more impressive.",
     "markers": ["one of us", "people like us tend to", "trust him more because he's from"],
     "text": "In-group bias: the tendency to favor members of one's own group over an out-group in evaluation or trust, often without rational basis. Example: two candidates gave identical answers, but the interviewer rated the one from her own university as more impressive."},
]

# Starter gold eval set: (passage, expected_bias_id or None, note).
# None means the passage should NOT trigger a flag -- keep some of these,
# your safety critic needs negative examples too, or you'll never catch
# false positives before the judges do.
EVAL_EXAMPLES = [
    {"id": "E01", "text": "We've put two years into this product, so we can't shut it down now, no matter what the numbers say.", "expected_bias_id": "B04", "note": "Sunk cost fallacy"},
    {"id": "E02", "text": "I'm certain the launch will go perfectly, we don't need a contingency plan.", "expected_bias_id": "B07", "note": "Overconfidence bias"},
    {"id": "E03", "text": "The lab results showed a 3% improvement in the treatment group compared to placebo, within the study's margin of error.", "expected_bias_id": None, "note": "Plain reporting of a stat -- no bias, careful negative example"},
    {"id": "E04", "text": "Everyone on the panel already agreed before I spoke, so I just went along with the decision instead of raising my concern.", "expected_bias_id": "B16", "note": "Groupthink"},
    {"id": "E05", "text": "The team reviewed three vendors, checked references for each, and chose the one with the strongest track record on similar projects.", "expected_bias_id": None, "note": "Sound decision process -- no bias, negative example"},
    {"id": "E06", "text": "After hearing about two dog attacks on the news this week, she decided all large dogs must be dangerous.", "expected_bias_id": "B03", "note": "Availability heuristic"},
]

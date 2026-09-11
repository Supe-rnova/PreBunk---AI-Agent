"""Step 3 check: run the fact-checker directly (no server needed)."""
import json

from fact_check import fact_check

SAMPLES = [
    ("expect false", "Scientists confirmed the Great Wall of China is easily visible from the Moon with the naked eye. Share with everyone!"),
    ("expect true", "Mount Everest is the highest mountain on Earth above sea level."),
    ("expect no claim", "This is DISGUSTING. You won't believe what they are doing to our children. Wake up people!!!"),
    ("expect unverified", "My neighbour's cousin said a new shop on MG Road is giving free phones to the first 100 people tomorrow."),
]

for label, text in SAMPLES:
    print(f"--- {label}: {text[:70]}")
    print(json.dumps(fact_check(text), indent=2, ensure_ascii=False))
    print()

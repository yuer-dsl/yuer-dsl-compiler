# ==================== reproducibility_test.py ====================
"""
This script tests reproducibility under fixed sampling conditions.

It performs 100 runs against a simple OpenAI prompt using:
temperature=0, seed=42

Verifies whether output hashes remain identical.
"""

import hashlib
import time
from openai import OpenAI

client = OpenAI()  # Provide API key via env var or config


def run_once():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Test reproducibility"}],
        temperature=0.0,
        top_p=1.0,
        seed=42,
    )
    output = response.choices[0].message.content.strip()
    return hashlib.sha256(output.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print("Running 100 reproducibility tests...\n")

    hashes = []
    for i in range(100):
        h = run_once()
        hashes.append(h)
        print(f"Run {i+1:3d} → {h}")
        time.sleep(0.05)

    print("\n--- Summary ---")
    if len(set(hashes)) == 1:
        print("100% IDENTICAL OUTPUT — deterministic sampling verified.")
        print("Signature:", hashes[0])
    else:
        print("Mismatch detected — nondeterministic behavior observed.")
        print(f"Unique hashes: {len(set(hashes))}")

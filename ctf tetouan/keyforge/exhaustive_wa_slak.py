#!/usr/bin/env python3
"""
Try exhaustive combinations with "wa slak ajmi" words
"""
import subprocess

def test_flag(content):
    try:
        result = subprocess.run(['./KeyForge'], input=f"DeepSec{{{content}}}\n",
                              capture_output=True, timeout=0.5, text=True)
        if "License valid!" in result.stdout:
            return "VALID"
        elif "validation failed" in result.stdout:
            return "FAILED"
        return "FORMAT"
    except:
        return "ERROR"

known = "wh0_s41d_y0"

# Generate all possible orderings and transformations of wa/slak/ajmi/regle
words = ["wa", "slak", "ajmi", "regle"]

# Different separators
seps = ["_", "", "-"]

# Leetspeak variations
leet = {
    "wa": ["wa", "w4", "wa_", "w4_"],
    "slak": ["slak", "sl4k", "5lak", "5l4k"],
    "ajmi": ["ajmi", "4jmi", "ajm1", "4jm1"],
    "regle": ["regle", "r3gle", "regl3", "r3gl3"],
}

patterns = []

# Try all combinations
for w1 in leet["wa"]:
    for w2 in leet["slak"]:
        for w3 in leet["ajmi"]:
            for sep in seps:
                # wa sep slak sep ajmi
                p = f"{w1}{sep}{w2}{sep}{w3}"
                if len(p) <= 16:
                    p = p + "_" * (16 - len(p))
                    if len(p) == 16 and p not in patterns:
                        patterns.append(p)
                
                # Try with regle
                for w4 in leet["regle"]:
                    p = f"{w1}{sep}{w2}{sep}{w3}{sep}{w4}"
                    if len(p) == 16 and p not in patterns:
                        patterns.append(p)
                    
                    # Try without wa
                    p = f"{w2}{sep}{w3}{sep}{w4}"
                    if len(p) <= 16:
                        p = p + "_" * (16 - len(p))
                        if len(p) == 16 and p not in patterns:
                            patterns.append(p)

print(f"Generated {len(patterns)} unique patterns to test...")

for i, pattern in enumerate(patterns, 1):
    full = known + pattern
    result = test_flag(full)
    
    if i % 50 == 0:
        print(f"[{i}/{len(patterns)}] Tested...")
    
    if result == "VALID":
        print(f"\n{'='*60}")
        print("FOUND THE FLAG!")
        print(f"{'='*60}")
        print(f"DeepSec{{{full}}}")
        print(f"{'='*60}")
        exit(0)
    elif result == "FORMAT":
        print(f"Format error on: {pattern}")

print(f"\nTested all {len(patterns)} patterns. None matched.")

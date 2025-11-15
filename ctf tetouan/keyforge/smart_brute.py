#!/usr/bin/env python3
"""
Smart brute force for remaining 16 characters using common CTF patterns
"""
import subprocess
import itertools

def test_flag(content):
    """Test a flag"""
    try:
        result = subprocess.run(['./KeyForge'], input=f"DeepSec{{{content}}}\n",
                              capture_output=True, timeout=0.5, text=True)
        output = result.stdout.strip()
        if "License valid!" in output:
            return "VALID"
        elif "License validation failed" in output:
            return "FAILED"
        return "FORMAT"
    except:
        return "ERROR"

known = "wh0_s41d_y0"  # 11 chars, need 16 more = 27 total

# Build smart patterns based on "who said you..."
# Common endings: cant crack/break me, could do this, are smart, etc

# 16-character patterns that make sense
patterns = [
    # Format: "who said you <16 chars>"
    "u_c4nt_br34k_m3",  # you cant break me
    "u_c4nt_s0lv3_m3",  # you cant solve me  
    "u_sh0uld_try_1t",  # you should try it
    "u_w0uld_try_th1s", # you would try this
    "u_c4n_s0lv3_th1s", # you can solve this
    "u_c0uld_pwn_th1s", # you could pwn this
    "u_w3r3_sm4rt_3h",  # you were smart eh
    "u_4r3_sm4rt_3n0",  # you are smart eno(ugh)
    "u_g0t_sk1lls_m8",  # you got skills m8
    "u_h4v3_sk1lls__",  # you have skills
    "u_c4n_r3v3rs3__",  # you can reverse
    "u_kn0w_crypt0__",  # you know crypto
]

print(f"Testing {len(patterns)} smart patterns...")
for i, ending in enumerate(patterns, 1):
    if len(ending) == 16:
        full = known + ending
        if len(full) == 27:
            result = test_flag(full)
            print(f"{i}. DeepSec{{{full}}} -> {result}")
            if result == "VALID":
                print(f"\n{'='*60}")
                print(f"FOUND THE FLAG!")
                print(f"{'='*60}")
                print(f"DeepSec{{{full}}}")
                break
        else:
            print(f"Skipping {ending} (wrong length: {len(full)})")
    else:
        print(f"Skipping {ending} (ending is {len(ending)} chars, need 16)")

print("\nDone!")

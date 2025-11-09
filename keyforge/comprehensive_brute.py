#!/usr/bin/env python3
"""
Comprehensive wordlist-based brute force
Generate all reasonable CTF-style 16-character completions
"""
import subprocess
import itertools

def test_flag(content):
    try:
        result = subprocess.run(['./KeyForge'], input=f"DeepSec{{{content}}}\n",
                              capture_output=True, timeout=0.5, text=True)
        if "License valid!" in result.stdout:
            return "VALID"
        elif "License validation failed" in result.stdout:
            return "FAILED"
        return "FORMAT"
    except:
        return "ERROR"

known = "wh0_s41d_y0"  

# Build comprehensive patterns - 16 chars each
# "who said you <16 chars>"

endings = []

# Common CTF words to combine
words = {
    'subject': ['u', 'you'],  # 1-3 chars
    'verb': ['can', 'cant', 'could', 'would', 'should', 'will', 'wont', 'may', 'might'],  # 3-6 chars
    'action': ['solve', 'crack', 'break', 'pwn', 'hack', 'beat', 'win', 'pass', 'decode', 'rev', 'get'],  # 3-6 chars  
    'object': ['me', 'this', 'it', 'that'],  # 2-4 chars
    'modifier': ['ever', 'easily', 'really', 'truly'],  # 4-6 chars
}

# Pre-made 16-char patterns
endings = [
    "u_could_hack_it_",  
    "u_cant_solve_it",
    "u_couldnt_do_it",
    "u_would_try_dis",
    "u_c4n_cr4ck_it_",
    "u_c4nt_cr4ck_1t",
    "u_c0uld_pwn_1t__",
    "u_sh0uld_h4ck_1t",
    "u_w0uldnt_try_1t",
    "u_c0uld_s0lv3_1t",
    "u_w1ll_f41l_h3r3",
    "u_4r3_g00d_3n0",
    "ucould_solve_it_",
    "ucant_crack_me__",
    "uc0uld_pwn_th1s_",
    "u_may_crack_dis_",
    "_could_hack_it__",
    "_cant_solve_me__",
    "_c0uld_d0_th1s__",
]

# Leet-speak variations
leet_map = {
    'a': ['a', '4'],
    'e': ['e', '3'],
    'i': ['i', '1'],
    'o': ['o', '0'],
    's': ['s', '5'],
    't': ['t', '7'],
}

def leetify(s, level=1):
    """Generate leet variations"""
    if level == 0:
        return [s]
    variations = [s]
    for old, news in leet_map.items():
        new_variations = []
        for v in variations:
            for n in news:
                new_variations.append(v.replace(old, n))
        variations = list(set(new_variations))
    return variations[:10]  # Limit variations

# Add more manual patterns
more_patterns = [
    "_cant_pwn_me_bruh",  # 16 chars starting with _
    "u_r_n0t_sm4rt___",
    "u_th1nk_ur_c00l_",
    "u_g0t_n0_ch4nc3_",
]

all_patterns = endings + more_patterns

# Remove duplicates and verify length
valid_patterns = []
for p in all_patterns:
    if len(p) == 16 and p not in valid_patterns:
        valid_patterns.append(p)

print(f"Testing {len(valid_patterns)} patterns...")
count = 0

for pattern in valid_patterns:
    count += 1
    full = known + pattern
    if len(full) != 27:
        print(f"ERROR: '{pattern}' creates {len(full)} chars!")
        continue
    
    result = test_flag(full)
    if count % 10 == 0:
        print(f"[{count}/{len(valid_patterns)}] Tested...")
    
    if result == "VALID":
        print(f"\n{'='*70}")
        print(f"FOUND THE FLAG!")
        print(f"{'='*70}")
        print(f"DeepSec{{{full}}}")
        print(f"{'='*70}")
        break
    elif result == "FORMAT":
        print(f"Format error: {pattern}")

print(f"\nCompleted testing {count} patterns.")

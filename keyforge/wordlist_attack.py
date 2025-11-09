#!/usr/bin/env python3
"""
Brute force approach - try to find the actual strings by testing combinations
"""
import itertools
import string

def custom_hash(data):
    """Custom hash from function at 0x1320"""
    result = 0
    key = 0x42
    for byte in data:
        result = (result << 8)
        key_rotated = ((key << 1) | (key >> 7)) & 0xff
        xored = byte ^ key_rotated
        result ^= xored
        key = key_rotated
    return result

def fnv1a_hash(data):
    """FNV-1a hash function"""
    hash_val = 0x811c9dc5
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * 0x01000193) & 0xffffffff
    return hash_val

target_custom = 0xf361227b3b
target_fnv = 0x2ca413b2

# Try wordlist approach with common CTF patterns
wordlist_5 = [
    "fr0m_", "wh0_n", "wh0_s", "wh4t_", "wh3r3",
    "us3r_", "fl4g_", "k3y_i", "h4sh_", "cr4ck",
    "br34k", "s0lv3", "pwn3d", "0wn3d", "h4x0r",
]

wordlist_6 = [
    "sa1d_y", "t0ld_m", "kn0ws_", "th1nks", "cr4cks",
    "h4x_th", "pwn_th", "s0lv3d", "br0k3n", "cr4ck3",
]

print("Searching for 5-byte string...")
for word in wordlist_5:
    if len(word) == 5:
        h = custom_hash(word.encode())
        if h == target_custom:
            print(f"FOUND (custom hash): '{word}' -> 0x{h:010x}")
            break
else:
    # Brute force with common chars
    chars = string.ascii_lowercase + string.digits + "_"
    print(f"Trying brute force with charset: {chars} ({len(chars)} chars)")
    print(f"Total combinations: {len(chars)**5} =  {len(chars)**5:,}")
    
    count = 0
    for combo in itertools.product(chars, repeat=5):
        test = ''.join(combo)
        h = custom_hash(test.encode())
        count += 1
        if count % 100000 == 0:
            print(f"Tried {count:,} combinations...", end='\r')
        if h == target_custom:
            print(f"\nFOUND: '{test}' -> 0x{h:010x}")
            break

print()
print("Searching for 6-byte string...")
for word in wordlist_6:
    if len(word) == 6:
        h = fnv1a_hash(word.encode())
        if h == target_fnv:
            print(f"FOUND (FNV-1a): '{word}' -> 0x{h:08x}")
            break
else:
    print("Not found in wordlist, would need larger brute force")

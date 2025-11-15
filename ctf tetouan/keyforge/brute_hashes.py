#!/usr/bin/env python3
"""
Brute force the FNV-1a hash and the custom hash
"""
import itertools
import string

def fnv1a_hash(data):
    """FNV-1a hash function"""
    hash_val = 0x811c9dc5
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * 0x01000193) & 0xffffffff
    return hash_val

def custom_hash(data):
    """Custom hash from function at 0x1320"""
    # xor with rotating 0x42
    result = 0
    key = 0x42
    for byte in data:
        result = (result << 8) & 0xffffffffffff
        key = ((key << 1) | (key >> 7)) & 0xff  # rol key, 1
        result ^= (byte ^ key)
    return result

# Target values
target_fnv = 0x2ca413b2  # For position 13-18 (6 bytes)
target_custom = 0xf361227b3b  # For position 8-12 (5 bytes)

print(f"Target FNV-1a: 0x{target_fnv:08x}")
print(f"Target custom: 0x{target_custom:012x}")
print()

# Brute force the custom hash (5 bytes at position 8-12)
print("Brute forcing 5-byte custom hash...")
charset = string.ascii_lowercase + " "

found_custom = None
for combo in itertools.product(charset, repeat=5):
    test_str = ''.join(combo)
    h = custom_hash(test_str.encode())
    if h == target_custom:
        print(f"FOUND custom hash: '{test_str}' -> 0x{h:012x}")
        found_custom = test_str
        break

if not found_custom:
    # Try with the hint
    test = "slak "
    h = custom_hash(test.encode())
    print(f"Test 'slak ': 0x{h:012x}")
    
print()

# Brute force FNV-1a (6 bytes at position 13-18)
print("Brute forcing 6-byte FNV-1a hash...")
found_fnv = None

# Try common patterns first
patterns = [
    "ajmi r",
    " ajmi ",
    "ajmi  ",
    " regle",
]

for pattern in patterns:
    if len(pattern) == 6:
        h = fnv1a_hash(pattern.encode())
        if h == target_fnv:
            print(f"FOUND FNV-1a: '{pattern}' -> 0x{h:08x}")
            found_fnv = pattern
            break

if found_custom and found_fnv:
    print(f"\n=== SOLUTION ===")
    print(f"Position 8-12:  '{found_custom}'")
    print(f"Position 13-18: '{found_fnv}'")

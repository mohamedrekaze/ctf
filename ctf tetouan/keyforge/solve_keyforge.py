#!/usr/bin/env python3
"""
Reverse engineered validation functions from KeyForge
"""
import struct
import itertools
import subprocess

def validate_func_13f0(input_bytes):
    """
    Validation function at 0x13f0
    Takes 6 bytes from position 0x13 (19 decimal)
    """
    if len(input_bytes) != 6:
        return None
    
    r8d = 0   # XOR accumulator
    esi = 0   # ADD accumulator
    edx = 1   # MULTIPLY accumulator
    
    for byte_val in input_bytes:
        # imul edx, byte
        edx = edx * byte_val
        
        # Modulo 65537 optimization
        r10d = edx
        rax = (r10d << 16) + r10d
        rax = (rax << 15) + r10d
        rax = rax >> 47
        r10d = (rax << 16) - rax
        edx = (edx - r10d) & 0xFFFF
        
        # add esi, byte
        esi += byte_val
        
        # xor r8d, byte
        r8d ^= byte_val
    
    # Final computation
    esi = (esi + edx) & 0xFFFFFFFF
    esi = (esi ^ r8d) & 0xFFFF
    result = (esi + 0x5555) & 0xFFFF
    
    return result

def validate_func_14a0(input_bytes):
    """
    Validation function at 0x14a0
    Takes 10 bytes from position 0x19 (25 decimal)
    """
    if len(input_bytes) != 10:
        return None
    
    # Lookup table from 0x2060
    table = bytes.fromhex("123456789abcdef01122334455667788")
    
    esi = 0xabcdef00
    
    for byte_val in input_bytes:
        high_nibble = (byte_val >> 4) & 0xF
        low_nibble = byte_val & 0xF
        
        val_low = table[low_nibble]
        val_high = table[high_nibble]
        
        temp = (val_low + esi) & 0xFFFFFFFF
        temp = ((temp << 3) | (temp >> 29)) & 0xFFFFFFFF  # ROL 3
        
        esi = temp ^ val_high
    
    return esi & 0xFFFFFFFF

# Target values
TARGET_13F0 = 0x6a09
TARGET_14A0 = 0x83129d2a

print("Reverse engineered validation functions!")
print(f"Function 0x13f0 target: 0x{TARGET_13F0:04x}")
print(f"Function 0x14a0 target: 0x{TARGET_14A0:08x}")
print()

# Now brute force to find the correct inputs
charset = "abcdefghijklmnopqrstuvwxyz0123456789_"

print("Brute forcing function 0x13f0 (6 bytes)...")
print("Testing common patterns first...")

# Common 6-byte patterns
patterns_6 = [
    "u_wa_g", "u_w4_g", "wa_ghe", "w4_ghe", "wa_gh3", "w4_gh3",
    "gher_s", "gh3r_s", "gher_5", "gh3r_5",
    "_wa_gh", "_w4_gh", "uwa_gh", "uw4_gh",
    "wagher", "w4gher", "w4gh3r", "waGHER",
]

found_6 = None
for pattern in patterns_6:
    if len(pattern) == 6:
        result = validate_func_13f0(pattern.encode())
        if result == TARGET_13F0:
            print(f"✓ FOUND for 0x13f0: '{pattern}' -> 0x{result:04x}")
            found_6 = pattern
            break

if not found_6:
    print("Common patterns failed. Trying systematic search...")
    # Try all 2-char combos + common 4-char endings
    prefixes = ["u_", "wa", "w4", "_w", "_u"]
    middles = ["wa", "w4", "gh", "g3", "he", "h3", "sl", "5l"]
    
    for p1 in prefixes:
        for p2 in middles:
            for p3 in middles:
                pattern = (p1 + p2 + p3)[:6]
                if len(pattern) == 6:
                    result = validate_func_13f0(pattern.encode())
                    if result == TARGET_13F0:
                        print(f"✓ FOUND for 0x13f0: '{pattern}' -> 0x{result:04x}")
                        found_6 = pattern
                        break
        if found_6:
            break

print()
print("Brute forcing function 0x14a0 (10 bytes)...")
print("Testing common patterns first...")

# Common 10-byte patterns  
patterns_10 = [
    "r_slak_ajm", "r_sl4k_ajm", "r_slak_4jm", "r_sl4k_4jm",
    "r_5lak_ajm", "r_5l4k_ajm", "r_5lak_4jm", "r_5l4k_4jm",
    "er_slak_aj", "er_sl4k_aj", "3r_slak_aj", "3r_sl4k_aj",
    "slak_ajmi_", "sl4k_ajmi_", "slak_4jmi_", "sl4k_4jmi_",
    "her_slak_a", "h3r_slak_a", "her_sl4k_a", "h3r_sl4k_a",
]

found_10 = None
for pattern in patterns_10:
    if len(pattern) == 10:
        result = validate_func_14a0(pattern.encode())
        if result == TARGET_14A0:
            print(f"✓ FOUND for 0x14a0: '{pattern}' -> 0x{result:08x}")
            found_10 = pattern
            break

if found_6 and found_10:
    print()
    print("="*60)
    print("SOLUTION FOUND!")
    print("="*60)
    known = "wh0_s41d_y0"
    flag = f"DeepSec{{{known}{found_6}{found_10}}}"
    print(f"Flag: {flag}")
    print("="*60)
    
    # Test it
    print("\nVerifying with actual binary...")
    result = subprocess.run(['./KeyForge'], input=flag + '\n',
                          capture_output=True, timeout=0.5, text=True)
    print(result.stdout)
else:
    print("\nNeed to expand search space...")

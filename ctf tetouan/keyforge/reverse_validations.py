#!/usr/bin/env python3
"""
Reverse engineer the remaining validation functions
"""
import struct

# Known values from data section
TARGET_AT_404C = 0x8309  # Target for function at 0x13f0 (after adding 0x5555: becomes 0x2db4 before adding)
TARGET_AT_4048 = 0x2a9d1283  # Actually need to read carefully

# From objdump -s -j .data:
# 4048: 2a9d1283 096a0000 b213a42c 00000000
# So at 0x4048: 0x2a, 0x9d, 0x12, 0x83

# Reading as little-endian DWORD at 0x4048:
TARGET_4048 = 0x83129d2a

print("Analyzing validation function at 0x13f0:")
print("This function validates 6 bytes at position 0x13 (19 decimal)")
print(f"Target value at 0x404c (word): 0x{TARGET_AT_404C:04x}")
print(f"After subtracting 0x5555 in code: 0x{TARGET_AT_404C - 0x5555:04x} = {TARGET_AT_404C - 0x5555}")
print()

print("Analyzing validation function at 0x14a0:")
print("This function validates 10 bytes at position 0x19 (25 decimal)")
print(f"Target value at 0x4048 (dword): 0x{TARGET_4048:08x}")
print()

# The lookup table from 0x2060
table_hex = "123456789abcdef01122334455667788736c616b20616a6d69207265676c6520"
table = bytes.fromhex(table_hex)
print(f"Lookup table (32 bytes): {table}")
print(f"Readable part: {table[16:].decode('ascii')}")
print()

# Function at 0x14a0 algorithm (from disassembly):
# 1. Copies 10 bytes from input+0x19 to stack+0x5
# 2. Loads 16-byte table from 0x2060 to stack+0x10  
# 3. For each byte in the 10-byte input:
#    - Split byte into high and low nibbles
#    - Look up table[high_nibble] and table[low_nibble]
#    - Perform: result = ((table[low] + prev_result) ROL 3) XOR table[high]
# 4. Compare final result with value at 0x4048

def validate_func_14a0(input_bytes):
    """
    Reverse engineered validation from 0x14a0
    """
    if len(input_bytes) != 10:
        return None
    
    # Initial value
    result = 0xabcdef00
    
    # Use first 16 bytes of table
    lookup = table[:16]
    
    for byte in input_bytes:
        high_nibble = (byte >> 4) & 0xf
        low_nibble = byte & 0xf
        
        # Get values from lookup table
        val_low = lookup[low_nibble]
        val_high = lookup[high_nibble]
        
        # Add and rotate
        temp = (val_low + result) & 0xffffffff
        temp = ((temp << 3) | (temp >> 29)) & 0xffffffff  # ROL 3
        
        # XOR
        result = temp ^ val_high
    
    return result & 0xffffffff

# Test with the readable string
test = b"slak ajmi "
print(f"Testing with '{test.decode()}': 0x{validate_func_14a0(test):08x}")
print()

# Try to brute force this - but 10 bytes is too much
# Let's see if the hint "slak ajmi regle " is actually used
print("Trying hint string variations:")
variations = [
    b"slak ajmi ",  # 10 bytes
    b"slakajmire",  # 10 bytes
    b"slak_ajmi_",  # 10 bytes
]

for v in variations:
    if len(v) == 10:
        result = validate_func_14a0(v)
        print(f"  '{v.decode()}': 0x{result:08x} (target: 0x{TARGET_4048:08x}) {'MATCH!' if result == TARGET_4048 else ''}")


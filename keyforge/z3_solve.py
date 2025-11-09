#!/usr/bin/env python3
"""
Solve KeyForge using Z3 constraint solver
Based on reverse engineering analysis
"""
from z3 import *
import struct

# Create Z3 solver
s = Solver()

# Create symbolic bytes for the flag content (positions 8-34, 27 bytes)
flag_bytes = [BitVec(f'flag_{i}', 8) for i in range(27)]

# Constraint 1: All bytes must be printable ASCII and match the allowed character set
# From the bit mask analysis: letters (A-Z, a-z) or special chars in range 0x21-0x5f  
# but excluding some characters. For simplicity, let's restrict to letters, digits, and common symbols
allowed_ranges = [
    (ord('A'), ord('Z')),
    (ord('a'), ord('z')),
    (ord('0'), ord('9')),
    (ord('_'), ord('_')),
    (ord('-'), ord('-')),
    (ord(' '), ord(' ')),
]

for b in flag_bytes:
    # Create OR condition for all allowed ranges
    range_conditions = []
    for start, end in allowed_ranges:
        range_conditions.append(And(b >= start, b <= end))
    s.add(Or(range_conditions))

# Constraint 2: Custom hash for bytes 0-4 (positions 8-12)
# Target: 0xf361227b3b
def custom_hash_z3(bytes_list):
    """Z3 version of the custom hash function"""
    result = BitVecVal(0, 64)
    key = BitVecVal(0x42, 8)
    
    for byte in bytes_list:
        result = result << 8
        # ROL key, 1
        key_rotated = ((key << 1) | (LShR(key, 7))) & 0xFF
        xored = byte ^ key_rotated
        result = result ^ ZeroExt(56, xored)
        key = key_rotated
    
    return result

hash1_target = 0xf361227b3b
hash1_result = custom_hash_z3(flag_bytes[0:5])
s.add(hash1_result == hash1_target)

# Constraint 3: FNV-1a hash for bytes 5-10 (positions 13-18)
# Target: 0x2ca413b2
def fnv1a_hash_z3(bytes_list):
    """Z3 version of FNV-1a hash"""
    h = BitVecVal(0x811c9dc5, 32)
    
    for byte in bytes_list:
        h = h ^ ZeroExt(24, byte)
        h = h * 0x01000193
    
    return h

hash2_target = 0x2ca413b2
hash2_result = fnv1a_hash_z3(flag_bytes[5:11])
s.add(hash2_result == hash2_target)

print("Solving constraints...")
print(f"Constraint 1: Printable ASCII")
print(f"Constraint 2: Custom hash for positions 8-12 = 0x{hash1_target:010x}")
print(f"Constraint 3: FNV-1a hash for positions 13-18 = 0x{hash2_target:08x}")
print()

# Try to solve
if s.check() == sat:
    print("=" * 60)
    print("SOLUTION FOUND!")
    print("=" * 60)
    
    m = s.model()
    
    # Extract the solution
    solution_bytes = []
    for i in range(27):
        val = m[flag_bytes[i]].as_long()
        solution_bytes.append(val)
    
    solution_str = ''.join(chr(b) for b in solution_bytes)
    full_flag = f"DeepSec{{{solution_str}}}"
    
    print(f"Flag: {full_flag}")
    print()
    
    # Verify with actual binary
    import subprocess
    result = subprocess.run(['./KeyForge'], input=full_flag.encode() + b'\n',
                          capture_output=True, timeout=2)
    print("Verification:")
    print(result.stdout.decode())
    
else:
    print("No solution found with current constraints.")
    print("The binary may have additional validation logic we haven't captured.")

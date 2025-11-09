#!/usr/bin/env python3
"""
Zaytron flag generator - reimplementation of the flag generation algorithm
"""

def generate_flag(seed):
    """Generate the flag based on the seed value"""
    flag = bytearray(56)  # 0x38 bytes total
    
    # All operations reference the seed at different byte positions and apply operations
    
    # Position 0: (seed >> 24) + 0x66
    flag[0] = ((seed >> 24) + 0x66) & 0xFF
    
    # Position 1: ((seed >> 16) & 0xFF) - 0x48
    flag[1] = (((seed >> 16) & 0xFF) - 0x48) & 0xFF
    
    # Position 2: copy from position 1
    flag[2] = flag[1]
    
    # Position 3: ((seed >> 8) & 0xFF) - 0x4e
    flag[3] = (((seed >> 8) & 0xFF) - 0x4e) & 0xFF
    
    # Position 4: (seed >> 24) + 0x75
    flag[4] = ((seed >> 24) + 0x75) & 0xFF
    
    # Position 5: copy from position 1
    flag[5] = flag[1]
    
    # Position 6: ((seed >> 16) & 0xFF) - 0x4a
    flag[6] = (((seed >> 16) & 0xFF) - 0x4a) & 0xFF
    
    # Position 7: (seed & 0xFF) - 0x74
    flag[7] = ((seed & 0xFF) - 0x74) & 0xFF
    
    # Position 8: copy from position 6
    flag[8] = flag[6]
    
    # Position 9: (seed % 100) - 0xb
    flag[9] = ((seed % 100) - 0xb) & 0xFF
    
    # Position 10: ((seed >> 16) & 0xFF) - 0x40
    flag[10] = (((seed >> 16) & 0xFF) - 0x40) & 0xFF
    
    # Position 11: copy from position 3
    flag[11] = flag[3]
    
    # Position 12: ((seed >> 8) & 0xFF) - 0x52
    flag[12] = (((seed >> 8) & 0xFF) - 0x52) & 0xFF
    
    # Position 13: (seed % 10) + 0x2a
    flag[13] = ((seed % 10) + 0x2a) & 0xFF
    
    # Position 14: ((seed >> 16) & 0xFF) - 0x35
    flag[14] = (((seed >> 16) & 0xFF) - 0x35) & 0xFF
    
    # Position 15: (seed % 100) + 0x24
    flag[15] = ((seed % 100) + 0x24) & 0xFF
    
    # Position 16: ((seed >> 8) & 0xFF) - 0x5c
    flag[16] = (((seed >> 8) & 0xFF) - 0x5c) & 0xFF
    
    # Position 17: (seed % 50) + 0x28
    flag[17] = ((seed % 50) + 0x28) & 0xFF
    
    # Position 18: ((seed >> 8) & 0xFF) - 0x4a
    flag[18] = (((seed >> 8) & 0xFF) - 0x4a) & 0xFF
    
    # Position 19: ((seed >> 8) & 0xFF) - 0x47
    flag[19] = (((seed >> 8) & 0xFF) - 0x47) & 0xFF
    
    # Position 20: copy from position 17
    flag[20] = flag[17]
    
    # Position 21: ((seed >> 16) & 0xFF) - 0x3a
    flag[21] = (((seed >> 16) & 0xFF) - 0x3a) & 0xFF
    
    # Position 22: copy from position 13
    flag[22] = flag[13]
    
    # Position 23: copy from position 15
    flag[23] = flag[15]
    
    # Position 24: copy from position 9
    flag[24] = flag[9]
    
    # Position 25: copy from position 3
    flag[25] = flag[3]
    
    # Position 26: copy from position 13
    flag[26] = flag[13]
    
    # Position 27: ((seed >> 8) & 0xFF) - 0x4c
    flag[27] = (((seed >> 8) & 0xFF) - 0x4c) & 0xFF
    
    # Position 28: (seed % 10) + 0x2b
    flag[28] = ((seed % 10) + 0x2b) & 0xFF
    
    # Position 29: copy from position 18
    flag[29] = flag[18]
    
    # Position 30: copy from position 17
    flag[30] = flag[17]
    
    # Position 31: copy from position 9
    flag[31] = flag[9]
    
    # Position 32: ((seed >> 16) & 0xFF) - 0x3f
    flag[32] = (((seed >> 16) & 0xFF) - 0x3f) & 0xFF
    
    # Position 33: copy from position 21
    flag[33] = flag[21]
    
    # Position 34: copy from position 15
    flag[34] = flag[15]
    
    # Position 35: copy from position 28
    flag[35] = flag[28]
    
    # Position 36: copy from position 27
    flag[36] = flag[27]
    
    # Position 37: copy from position 13
    flag[37] = flag[13]
    
    # Position 38: copy from position 15
    flag[38] = flag[15]
    
    # Position 39: ((seed >> 8) & 0xFF) - 0x58
    flag[39] = (((seed >> 8) & 0xFF) - 0x58) & 0xFF
    
    # Position 40: ((seed >> 8) & 0xFF) - 0x49
    flag[40] = (((seed >> 8) & 0xFF) - 0x49) & 0xFF
    
    # Position 41: copy from position 32
    flag[41] = flag[32]
    
    # Position 42: copy from position 15
    flag[42] = flag[15]
    
    # Position 43: copy from position 18
    flag[43] = flag[18]
    
    # Position 44: copy from position 9
    flag[44] = flag[9]
    
    # Position 45: copy from position 15
    flag[45] = flag[15]
    
    # Position 46: copy from position 27
    flag[46] = flag[27]
    
    # Position 47: copy from position 13
    flag[47] = flag[13]
    
    # Position 48: ((seed >> 8) & 0xFF) - 0x48
    flag[48] = (((seed >> 8) & 0xFF) - 0x48) & 0xFF
    
    # Position 49: copy from position 13
    flag[49] = flag[13]
    
    # Position 50: copy from position 27
    flag[50] = flag[27]
    
    # Position 51: copy from position 21
    flag[51] = flag[21]
    
    # Position 52: copy from position 13
    flag[52] = flag[13]
    
    # Position 53: (seed % 100) - 0x1a
    flag[53] = ((seed % 100) - 0x1a) & 0xFF
    
    # Position 54: (seed & 0xFF) - 0x72
    flag[54] = ((seed & 0xFF) - 0x72) & 0xFF
    
    # Position 55: null terminator
    flag[55] = 0
    
    # Return as string (excluding null terminator)
    return flag[:55].decode('latin-1', errors='ignore')

if __name__ == '__main__':
    seed = 0xdeadbeef
    flag = generate_flag(seed)
    print(f"Seed: 0x{seed:x} ({seed})")
    print(f"Generated flag: {flag}")
    print(f"Flag length: {len(flag)}")
    
    # Print as hex for debugging
    print(f"Hex: {' '.join(f'{ord(c):02x}' for c in flag)}")

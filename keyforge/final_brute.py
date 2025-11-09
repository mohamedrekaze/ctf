#!/usr/bin/env python3
"""
Brute force remaining characters position by position against the actual binary
"""
import subprocess
import string
import sys

def test_flag(flag):
    """Test a flag and return the result"""
    try:
        result = subprocess.run(['./KeyForge'], input=flag + '\n',
                              capture_output=True, timeout=0.5, text=True)
        output = result.stdout.strip()
        if "License valid!" in output:
            return "VALID"
        elif "License validation failed" in output:
            return "FAILED"
        elif "Invalid format" in output:
            return "FORMAT"
        return "UNKNOWN"
    except:
        return "ERROR"

# Known so far: DeepSec{wh0_s41d_y0XXXXXXXXXXXXXXXXX}
#                        01234567890123456789012345678901234
#                                  111111111122222222223333

known = "wh0_s41d_y0"  # Positions 8-18 (11 chars)
remaining = 16  # Need 16 more chars (positions 19-34)

# Charset to try (letters, digits, underscore, space)
charset = string.ascii_lowercase + string.digits + "_" + "u"  # 'u' for "you"

print(f"Known prefix: DeepSec{{{known}}}")
print(f"Need to find: {remaining} more characters")
print(f"Charset: {charset}")
print()

# Try common CTF endings and patterns
patterns = [
    "u_c4nt_cr4ck_m3",  # 16 chars
    "u_c4n7_cr4ck_m3",  # 16 chars
    "ucantcrackme____",  # 16 chars
    "cant_crack_me___",  # 16 chars (without 'u')
]

for pattern in patterns:
    if len(pattern) == remaining:
        flag = f"DeepSec{{{known}{pattern}}}"
        result = test_flag(flag)
        print(f"Trying: {flag}")
        print(f"Result: {result}")
        if result == "VALID":
            print(f"\n{'='*60}")
            print("FOUND THE FLAG!")
            print(f"{'='*60}")
            print(flag)
            sys.exit(0)

print("\nPatterns didn't work. Starting character-by-character brute force...")
print("This will test each position independently.")

# Brute force position by position
current = known
for pos in range(len(known), 27):
    print(f"\nPosition {pos} (character {pos-7} inside braces):")
    found_char = None
    
    for char in charset:
        test = current + char + "A" * (27 - len(current) - 1)
        flag = f"DeepSec{{{test}}}"
        result = test_flag(flag)
        
        if result == "VALID":
            found_char = char
            print(f"  '{char}': VALID! Found the complete flag!")
            current += char
            break
        elif result == "FAILED":
            # Still failing but passed format - might be correct char
            print(f"  '{char}': FAILED", end='')
        
    if found_char:
        current += found_char
        print(f"\nCurrent: {current}")
    else:
        print(f"\nCould not determine character at position {pos}")
        print(f"Current best guess: {current}")
        break

final_flag = f"DeepSec{{{current}}}"
print(f"\n{'='*60}")
print(f"Final result: {final_flag}")
print(f"{'='*60}")

# Final test
result = test_flag(final_flag)
print(f"Validation: {result}")

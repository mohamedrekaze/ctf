#!/usr/bin/env python3
"""
KeyForge reverse engineering script
"""
import subprocess
import string

def test_input(inp):
    """Test an input against the binary"""
    try:
        result = subprocess.run(
            ['./KeyForge'],
            input=inp + '\n',
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout + result.stderr
    except:
        return ""

# Test various formats
print("Testing formats...")
formats = [
    "DeepSec{test}",
    "XXXX-XXXX-XXXX-XXXX",
    "slak ajmi regle ",
    "slak-ajmi-regle-",
    "slak ajmi regle",
]

for fmt in formats:
    output = test_input(fmt)
    print(f"\nInput: {repr(fmt)}")
    print(f"Output: {output.strip()}")

#!/usr/bin/env python3
"""
Analyze the KeyForge binary
"""
import subprocess
import sys

def run_binary(input_str):
    """Run the binary with given input"""
    try:
        result = subprocess.run(
            ['./KeyForge'],
            input=input_str + '\n',
            capture_output=True,
            text=True,
            timeout=2,
            cwd='/workspaces/ctf/ctf_rabat/keyforge'
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

# Test basic input
print("Testing basic inputs...")
tests = [
    "VoidBox{test}",
    "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}",
    "test",
    "",
]

for test in tests:
    print(f"\n{'='*60}")
    print(f"Input: {repr(test)}")
    stdout, stderr = run_binary(test)
    print(f"STDOUT: {stdout}")
    if stderr:
        print(f"STDERR: {stderr}")

# Extract strings from binary
print("\n" + "="*60)
print("Extracting strings from binary...")
try:
    result = subprocess.run(
        ['strings', '/workspaces/ctf/ctf_rabat/keyforge/KeyForge'],
        capture_output=True,
        text=True,
        timeout=5
    )
    strings_output = result.stdout
    print("Interesting strings:")
    for line in strings_output.split('\n'):
        if any(keyword in line.lower() for keyword in ['void', 'flag', 'license', 'key', 'valid', 'enter', 'correct']):
            print(f"  {line}")
except Exception as e:
    print(f"Error: {e}")

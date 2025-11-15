#!/usr/bin/env python3
"""
Solve KeyForge CTF challenge
"""
import subprocess
import os

# Make binary executable
binary_path = '/workspaces/ctf/ctf_rabat/keyforge/KeyForge'
os.chmod(binary_path, 0o755)

print("Extracting strings from binary...")
result = subprocess.run(['strings', binary_path], capture_output=True, text=True)
all_strings = result.stdout.split('\n')

print("\nAll strings in binary:")
print("="*60)
for s in all_strings:
    if s.strip():
        print(s)

print("\n" + "="*60)
print("Testing binary with sample input...")

def test_input(inp):
    """Test an input"""
    try:
        result = subprocess.run(
            [binary_path],
            input=inp + '\n',
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

# Test the example from instructions
test_flag = "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}"
stdout, stderr = test_input(test_flag)
print(f"\nTesting: {test_flag}")
print(f"STDOUT: {stdout}")
if stderr:
    print(f"STDERR: {stderr}")

# Test simple format
stdout, stderr = test_input("VoidBox{test}")
print(f"\nTesting: VoidBox{{test}}")
print(f"STDOUT: {stdout}")
if stderr:
    print(f"STDERR: {stderr}")

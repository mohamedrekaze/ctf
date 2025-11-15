#!/usr/bin/env python3
"""
Complete KeyForge solver for VoidBox CTF
"""
import subprocess
import os
import sys

binary_path = '/workspaces/ctf/ctf_rabat/keyforge/KeyForge'

# Make executable
try:
    os.chmod(binary_path, 0o755)
    print("[+] Made binary executable")
except Exception as e:
    print(f"[-] Error making executable: {e}")

# Step 1: Extract strings
print("\n[*] Extracting strings from binary...")
try:
    result = subprocess.run(['strings', binary_path], capture_output=True, text=True, timeout=5)
    strings_list = [s for s in result.stdout.split('\n') if s.strip()]
    
    print(f"[+] Found {len(strings_list)} strings")
    print("\n[*] Interesting strings:")
    for s in strings_list:
        if len(s) > 3:
            print(f"    {s}")
except Exception as e:
    print(f"[-] Error extracting strings: {e}")

# Step 2: Check file type
print("\n[*] Checking binary type...")
try:
    result = subprocess.run(['file', binary_path], capture_output=True, text=True)
    print(f"[+] {result.stdout.strip()}")
except Exception as e:
    print(f"[-] Error: {e}")

# Step 3: Test basic execution
print("\n[*] Testing binary execution...")
def test_flag(flag_str):
    """Test a flag"""
    try:
        result = subprocess.run(
            [binary_path],
            input=flag_str.encode() + b'\n',
            capture_output=True,
            timeout=2
        )
        stdout = result.stdout.decode('utf-8', errors='ignore')
        stderr = result.stderr.decode('utf-8', errors='ignore')
        return stdout, stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:
        return "", str(e), -1

# Test various inputs
test_inputs = [
    "test",
    "VoidBox{test}",
    "VoidBox{a" + "a"*50 + "}",
    "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}",
]

for inp in test_inputs:
    stdout, stderr, rc = test_flag(inp)
    print(f"\n  Input: {inp[:60]}...")
    print(f"  Return code: {rc}")
    if stdout:
        print(f"  STDOUT: {stdout[:200]}")
    if stderr and stderr != "TIMEOUT":
        print(f"  STDERR: {stderr[:200]}")

# Step 4: Try disassembly
print("\n[*] Attempting objdump disassembly...")
try:
    result = subprocess.run(
        ['objdump', '-d', binary_path],
        capture_output=True,
        text=True,
        timeout=10
    )
    lines = result.stdout.split('\n')
    print(f"[+] Disassembly has {len(lines)} lines")
    
    # Look for main function
    in_main = False
    main_lines = []
    for line in lines:
        if '<main>' in line:
            in_main = True
        if in_main:
            main_lines.append(line)
            if len(main_lines) > 100:  # First 100 lines of main
                break
    
    if main_lines:
        print("\n[*] First part of main function:")
        for line in main_lines[:50]:
            print(line)
            
except Exception as e:
    print(f"[-] Error: {e}")

print("\n" + "="*60)
print("[*] Analysis complete. Review output above.")

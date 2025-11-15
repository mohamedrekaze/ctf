#!/usr/bin/env python3
"""
KeyForge solver - extract and reverse engineer validation
Since terminal is stuck, this will write results to files
"""
import subprocess
import os
import sys

BINARY = '/workspaces/ctf/ctf_rabat/keyforge/KeyForge'
OUTPUT_FILE = '/workspaces/ctf/ctf_rabat/keyforge/solver_output.txt'

def log(msg):
    """Log to both stdout and file"""
    print(msg)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(msg + '\n')

# Clear output file
open(OUTPUT_FILE, 'w').close()

# Make executable
os.chmod(BINARY, 0o755)
log("[+] Made binary executable")

# Extract strings
log("\n[*] Extracting strings from binary...")
try:
    result = subprocess.run(['strings', BINARY], capture_output=True, text=True, timeout=5)
    all_strings = result.stdout.split('\n')
    log(f"[+] Found {len(all_strings)} strings")
    
    # Find interesting ones
    interesting = []
    for s in all_strings:
        s_lower = s.lower()
        if any(kw in s_lower for kw in ['enter', 'license', 'key', 'valid', 'format', 'void', 'correct', 'wrong', 'success', 'fail', 'invalid']):
            interesting.append(s)
    
    if interesting:
        log("\n[+] Interesting strings found:")
        for s in interesting:
            log(f"    {s}")
    
    # Save all strings
    with open('/workspaces/ctf/ctf_rabat/keyforge/all_strings.txt', 'w') as f:
        f.write('\n'.join(all_strings))
    log("[+] Saved all strings to all_strings.txt")
    
except Exception as e:
    log(f"[-] Error extracting strings: {e}")

# Test inputs
log("\n[*] Testing binary with various inputs...")

test_cases = [
    ("Example from instructions", "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}"),
    ("Simple test", "VoidBox{test}"),
    ("Empty content", "VoidBox{}"),
    ("Just format", "VoidBox"),
]

for name, test_input in test_cases:
    log(f"\n  [{name}]")
    log(f"  Input: {test_input[:70]}")
    try:
        result = subprocess.run(
            [BINARY],
            input=test_input.encode() + b'\n',
            capture_output=True,
            timeout=2
        )
        stdout = result.stdout.decode('utf-8', errors='ignore').strip()
        stderr = result.stderr.decode('utf-8', errors='ignore').strip()
        
        log(f"  Return code: {result.returncode}")
        if stdout:
            log(f"  STDOUT: {stdout}")
        if stderr:
            log(f"  STDERR: {stderr}")
        
        # Check for success indicators
        if any(word in stdout.lower() for word in ['valid', 'correct', 'success', 'congratulations', 'flag']):
            log(f"\n{'='*60}")
            log(f"POSSIBLE FLAG FOUND: {test_input}")
            log(f"{'='*60}")
            
    except Exception as e:
        log(f"  Error: {e}")

# Get disassembly
log("\n[*] Extracting disassembly...")
try:
    result = subprocess.run(['objdump', '-d', '-M', 'intel', BINARY], 
                          capture_output=True, text=True, timeout=30)
    disasm = result.stdout
    
    with open('/workspaces/ctf/ctf_rabat/keyforge/disasm.txt', 'w') as f:
        f.write(disasm)
    
    log(f"[+] Saved {len(disasm.split(chr(10)))} lines of disassembly to disasm.txt")
    
except Exception as e:
    log(f"[-] Error: {e}")

log(f"\n[*] Analysis complete. Check {OUTPUT_FILE} and disasm.txt for details.")
print(f"\nResults written to: {OUTPUT_FILE}")

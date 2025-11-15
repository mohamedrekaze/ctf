#!/usr/bin/env python3
"""
Comprehensive KeyForge solver for VoidBox CTF
"""
import subprocess
import os
import sys
import re
import itertools
import string

BINARY = '/workspaces/ctf/ctf_rabat/keyforge/KeyForge'

def run_binary(input_str):
    """Run the binary with given input"""
    try:
        result = subprocess.run(
            [BINARY],
            input=input_str.encode() + b'\n',
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

def extract_strings():
    """Extract all strings from binary"""
    try:
        result = subprocess.run(['strings', BINARY], capture_output=True, text=True, timeout=5)
        return result.stdout.split('\n')
    except:
        return []

def get_disassembly():
    """Get objdump disassembly"""
    try:
        result = subprocess.run(['objdump', '-d', '-M', 'intel', BINARY], 
                              capture_output=True, text=True, timeout=30)
        return result.stdout
    except:
        return ""

def analyze_binary():
    """Analyze the binary"""
    print("="*60)
    print("KEYFORGE BINARY ANALYSIS")
    print("="*60)
    
    # Step 1: Extract strings
    print("\n[*] Extracting strings...")
    all_strings = extract_strings()
    interesting = [s for s in all_strings if any(kw in s.lower() for kw in 
                   ['enter', 'license', 'key', 'valid', 'format', 'void', 'flag', 'correct', 'wrong'])]
    
    print(f"[+] Found {len(all_strings)} total strings")
    if interesting:
        print("[+] Interesting strings:")
        for s in interesting[:20]:
            print(f"    {s}")
    
    # Step 2: Test basic inputs
    print("\n[*] Testing binary with sample inputs...")
    test_cases = [
        "test",
        "VoidBox{test}",
        "VoidBox{" + "a"*50 + "}",
        "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}",
    ]
    
    for tc in test_cases:
        stdout, stderr, rc = run_binary(tc)
        print(f"\n  Input: {tc[:60]}")
        print(f"  RC: {rc}")
        if stdout.strip():
            print(f"  OUT: {stdout.strip()}")
    
    # Step 3: Get disassembly
    print("\n[*] Disassembling binary...")
    disasm = get_disassembly()
    
    if not disasm:
        print("[-] Could not disassemble binary")
        return None
    
    print(f"[+] Got {len(disasm.split(chr(10)))} lines of disassembly")
    
    # Look for main function
    main_match = re.search(r'<main>:.*?(?=\n\n|\n[0-9a-f]+\s+<)', disasm, re.DOTALL)
    if main_match:
        main_code = main_match.group(0)
        print("\n[*] Main function (first 100 lines):")
        for line in main_code.split('\n')[:100]:
            print(line)
    
    return disasm

def reverse_engineer():
    """Reverse engineer the validation"""
    print("\n" + "="*60)
    print("REVERSE ENGINEERING")
    print("="*60)
    
    # Based on the tetouan KeyForge, this binary likely has similar structure
    # Let's try to extract validation logic
    
    disasm = get_disassembly()
    if not disasm:
        print("[-] No disassembly available")
        return None
    
    # Save disassembly for manual inspection
    with open('/workspaces/ctf/ctf_rabat/keyforge/disasm.txt', 'w') as f:
        f.write(disasm)
    print("[+] Saved full disassembly to disasm.txt")
    
    # Look for comparison values and hash targets
    print("\n[*] Searching for comparison values in disassembly...")
    
    # Find immediate values that might be hash targets
    immediates = re.findall(r'\$0x([0-9a-f]+)', disasm)
    unique_imms = sorted(set(imm for imm in immediates if len(imm) >= 4))
    
    print(f"[+] Found {len(unique_imms)} unique immediate values (potential targets):")
    for imm in unique_imms[:30]:
        print(f"    0x{imm}")
    
    return disasm

def brute_force_approach():
    """Try brute force with common patterns"""
    print("\n" + "="*60)
    print("BRUTE FORCE APPROACH")
    print("="*60)
    
    # Based on the example format, try variations
    print("\n[*] Testing format variations...")
    
    # The example shows: VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}
    # Let's test if this is actually the flag
    
    test_flags = [
        "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}",
        "VoidBox{test}",
        "VoidBox{CTF}",
    ]
    
    for flag in test_flags:
        stdout, stderr, rc = run_binary(flag)
        print(f"\nTesting: {flag[:60]}...")
        print(f"  Return code: {rc}")
        if stdout:
            print(f"  Output: {stdout.strip()}")
            if 'valid' in stdout.lower() or 'correct' in stdout.lower() or 'success' in stdout.lower():
                print(f"\n{'='*60}")
                print(f"FOUND FLAG: {flag}")
                print(f"{'='*60}")
                return flag
    
    return None

if __name__ == "__main__":
    # Make binary executable
    os.chmod(BINARY, 0o755)
    
    # Run analysis
    analyze_binary()
    
    # Reverse engineer
    reverse_engineer()
    
    # Try brute force
    flag = brute_force_approach()
    
    if flag:
        print(f"\n\n{'='*60}")
        print(f"SUCCESS! FLAG: {flag}")
        print(f"{'='*60}")
    else:
        print("\n\n[*] Need deeper analysis. Check disasm.txt for details.")
        print("[*] Will need to implement hash functions from disassembly.")

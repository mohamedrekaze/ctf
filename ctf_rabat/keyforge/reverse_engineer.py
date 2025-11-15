#!/usr/bin/env python3
"""
KeyForge Reverse Engineering Script
Analyzes the binary to understand validation logic
"""
import subprocess
import re
import os
from pathlib import Path

BINARY_PATH = "/workspaces/ctf/ctf_rabat/keyforge/KeyForge"
OUTPUT_DIR = "/workspaces/ctf/ctf_rabat/keyforge"

def run_cmd(cmd, timeout=10):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, 
                              text=True, timeout=timeout, cwd=OUTPUT_DIR)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:
        return "", str(e), -1

def extract_strings():
    """Extract and analyze strings from binary"""
    print("[*] Extracting strings from binary...")
    
    stdout, stderr, rc = run_cmd(f"strings {BINARY_PATH}")
    if rc != 0:
        print(f"[-] Error extracting strings: {stderr}")
        return []
    
    strings = [s.strip() for s in stdout.split('\n') if s.strip()]
    print(f"[+] Found {len(strings)} strings")
    
    # Save all strings
    with open(f"{OUTPUT_DIR}/all_strings.txt", 'w') as f:
        f.write('\n'.join(strings))
    
    # Find interesting strings
    interesting = []
    keywords = ['enter', 'license', 'key', 'valid', 'invalid', 'format', 'void', 
                'correct', 'wrong', 'success', 'fail', 'error', 'flag']
    
    for s in strings:
        if any(kw in s.lower() for kw in keywords):
            interesting.append(s)
    
    print("[+] Interesting strings:")
    for s in interesting:
        print(f"    {s}")
    
    return strings

def get_disassembly():
    """Get full disassembly of the binary"""
    print("\n[*] Disassembling binary...")
    
    stdout, stderr, rc = run_cmd(f"objdump -d -M intel {BINARY_PATH}")
    if rc != 0:
        print(f"[-] Error disassembling: {stderr}")
        return ""
    
    # Save disassembly
    with open(f"{OUTPUT_DIR}/disassembly.txt", 'w') as f:
        f.write(stdout)
    
    lines = stdout.split('\n')
    print(f"[+] Generated {len(lines)} lines of disassembly")
    
    return stdout

def analyze_main_function(disasm):
    """Extract and analyze main function"""
    print("\n[*] Analyzing main function...")
    
    # Find main function
    main_match = re.search(r'<main>:.*?(?=\n\n|\n[0-9a-f]+\s+<)', disasm, re.DOTALL)
    if not main_match:
        print("[-] Could not find main function")
        return
    
    main_code = main_match.group(0)
    lines = main_code.split('\n')
    
    print(f"[+] Main function has {len(lines)} lines")
    
    # Save main function
    with open(f"{OUTPUT_DIR}/main_function.txt", 'w') as f:
        f.write(main_code)
    
    # Look for key patterns
    print("\n[+] Key patterns in main:")
    
    # Find function calls
    calls = re.findall(r'call\s+([0-9a-f]+)\s+<([^>]+)>', main_code)
    if calls:
        print("  Function calls:")
        for addr, name in calls:
            print(f"    {addr}: {name}")
    
    # Find immediate values (potential targets)
    immediates = re.findall(r'\$0x([0-9a-f]{4,})', main_code)
    if immediates:
        print("  Immediate values (potential hash targets):")
        for imm in set(immediates):
            print(f"    0x{imm}")
    
    # Find string references
    string_refs = re.findall(r'lea\s+.*,0x([0-9a-f]+)', main_code)
    if string_refs:
        print("  String references:")
        for ref in set(string_refs):
            print(f"    0x{ref}")

def find_validation_functions(disasm):
    """Find and analyze validation functions"""
    print("\n[*] Looking for validation functions...")
    
    # Find all functions
    functions = re.findall(r'([0-9a-f]+)\s+<([^>]+)>:', disasm)
    
    print(f"[+] Found {len(functions)} functions:")
    validation_funcs = []
    
    for addr, name in functions:
        print(f"  {addr}: {name}")
        if any(kw in name.lower() for kw in ['valid', 'check', 'hash', 'cmp']):
            validation_funcs.append((addr, name))
    
    # Extract validation function code
    for addr, name in validation_funcs:
        print(f"\n[*] Extracting function {name} at {addr}")
        func_pattern = rf'{addr}\s+<{re.escape(name)}>:.*?(?=\n\n|\n[0-9a-f]+\s+<)'
        func_match = re.search(func_pattern, disasm, re.DOTALL)
        
        if func_match:
            func_code = func_match.group(0)
            with open(f"{OUTPUT_DIR}/func_{name}_{addr}.txt", 'w') as f:
                f.write(func_code)
            print(f"[+] Saved function to func_{name}_{addr}.txt")

def analyze_data_section():
    """Analyze data section for hash targets"""
    print("\n[*] Analyzing data section...")
    
    stdout, stderr, rc = run_cmd(f"objdump -s -j .data {BINARY_PATH}")
    if rc == 0:
        with open(f"{OUTPUT_DIR}/data_section.txt", 'w') as f:
            f.write(stdout)
        print("[+] Saved data section to data_section.txt")
        
        # Look for potential hash targets
        hex_values = re.findall(r'([0-9a-f]{8})', stdout)
        if hex_values:
            print("[+] Potential hash targets in data section:")
            for val in set(hex_values):
                if val != '00000000':
                    print(f"    0x{val}")

def test_format_variations():
    """Test different input formats to understand expected format"""
    print("\n[*] Testing input format variations...")
    
    test_cases = [
        ("VoidBox{test}", "Standard VoidBox format"),
        ("DeepSec{test}", "DeepSec format (from tetouan)"),
        ("test", "Plain text"),
        ("VoidBox{}", "Empty VoidBox"),
        ("VoidBox{a}", "Single char"),
        ("VoidBox{" + "a"*27 + "}", "27 chars (like tetouan)"),
        ("VoidBox{" + "a"*50 + "}", "50 chars"),
        ("XXXX-XXXX-XXXX-XXXX", "License key format"),
    ]
    
    results = []
    for test_input, description in test_cases:
        stdout, stderr, rc = run_cmd(f'echo "{test_input}" | {BINARY_PATH}')
        results.append((test_input, description, stdout.strip(), rc))
        print(f"  {description}: {stdout.strip()}")
    
    # Save test results
    with open(f"{OUTPUT_DIR}/format_tests.txt", 'w') as f:
        for test_input, desc, output, rc in results:
            f.write(f"{desc}:\n")
            f.write(f"  Input: {test_input}\n")
            f.write(f"  Output: {output}\n")
            f.write(f"  Return Code: {rc}\n\n")

def main():
    """Main reverse engineering process"""
    print("="*60)
    print("KEYFORGE REVERSE ENGINEERING")
    print("="*60)
    
    # Make binary executable
    os.chmod(BINARY_PATH, 0o755)
    
    # Extract strings
    strings = extract_strings()
    
    # Get disassembly
    disasm = get_disassembly()
    
    if disasm:
        # Analyze main function
        analyze_main_function(disasm)
        
        # Find validation functions
        find_validation_functions(disasm)
    
    # Analyze data section
    analyze_data_section()
    
    # Test format variations
    test_format_variations()
    
    print(f"\n{'='*60}")
    print("REVERSE ENGINEERING COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved in: {OUTPUT_DIR}/")
    print("- all_strings.txt: All strings from binary")
    print("- disassembly.txt: Full disassembly")
    print("- main_function.txt: Main function code")
    print("- data_section.txt: Data section dump")
    print("- format_tests.txt: Input format test results")
    print("- func_*.txt: Individual function disassemblies")

if __name__ == "__main__":
    main()
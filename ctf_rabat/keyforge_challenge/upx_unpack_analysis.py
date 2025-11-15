#!/usr/bin/env python3
"""
UPX Unpacker and Advanced Analysis
"""
import subprocess
import os
import re

def run_cmd(cmd, input_data=None):
    """Run a command and return output"""
    try:
        if input_data:
            result = subprocess.run(cmd, shell=True, input=input_data.encode(), 
                                  capture_output=True, timeout=10)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, 
                                  text=True, timeout=10)
        
        stdout = result.stdout.decode('utf-8', errors='ignore') if isinstance(result.stdout, bytes) else result.stdout
        stderr = result.stderr.decode('utf-8', errors='ignore') if isinstance(result.stderr, bytes) else result.stderr
        return stdout, stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def main():
    print("UPX Unpacking and Advanced Analysis")
    print("="*50)
    
    # Step 1: Unpack UPX
    print("[1] Unpacking UPX...")
    stdout, stderr, rc = run_cmd("upx -d KeyForge -o KeyForge_unpacked")
    
    if rc == 0:
        print("[+] UPX unpacking successful!")
        binary = "KeyForge_unpacked"
        os.chmod(binary, 0o755)
    else:
        print("[-] UPX unpacking failed, using original binary")
        binary = "KeyForge"
    
    # Step 2: Extract strings from unpacked binary
    print(f"\n[2] Extracting strings from {binary}...")
    stdout, stderr, rc = run_cmd(f"strings {binary}")
    
    if rc == 0:
        all_strings = stdout.split('\n')
        interesting_strings = []
        
        # Look for validation-related strings
        keywords = ['enter', 'license', 'key', 'valid', 'invalid', 'format', 'void', 
                   'deep', 'sec', 'flag', 'correct', 'wrong', 'success', 'fail']
        
        for s in all_strings:
            if any(kw in s.lower() for kw in keywords) and len(s.strip()) > 2:
                interesting_strings.append(s.strip())
        
        print(f"[+] Found {len(all_strings)} strings total")
        print(f"[+] Found {len(interesting_strings)} interesting strings:")
        for s in interesting_strings:
            print(f"    '{s}'")
        
        # Save strings
        with open("unpacked_strings.txt", "w") as f:
            for s in all_strings:
                if s.strip():
                    f.write(s.strip() + "\n")
    
    # Step 3: Get disassembly of unpacked binary  
    print(f"\n[3] Disassembling {binary}...")
    stdout, stderr, rc = run_cmd(f"objdump -d -M intel {binary}")
    
    if rc == 0:
        with open("unpacked_disasm.txt", "w") as f:
            f.write(stdout)
        
        print(f"[+] Saved disassembly to unpacked_disasm.txt")
        
        # Look for validation functions
        lines = stdout.split('\n')
        functions = []
        
        for line in lines:
            if re.match(r'^[0-9a-f]+\s+<[^>]+>:', line):
                match = re.search(r'^([0-9a-f]+)\s+<([^>]+)>:', line)
                if match:
                    addr, name = match.groups()
                    functions.append((addr, name))
        
        print(f"\n[+] Found {len(functions)} functions:")
        for addr, name in functions:
            print(f"    {addr}: {name}")
    
    # Step 4: Test more format variations now that we know VoidBox{27} works
    print(f"\n[4] Testing VoidBox format variations...")
    
    # We know VoidBox{27 chars} gives "License validation failed"
    # Let's try different 27-char patterns
    test_patterns = [
        "VoidBox{" + "a"*27 + "}",  # We know this gives validation failed
        "VoidBox{" + "Welcome_To_our_Hummble_Ct" + "}",  # Part of instructions
        "VoidBox{" + "abcdefghijklmnopqrstuvwxyz1" + "}",  # alphabet + 1
        "VoidBox{" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ1" + "}",  # uppercase
        "VoidBox{" + "123456789012345678901234567" + "}",  # numbers
        "VoidBox{" + "test_flag_here_1234567890a" + "}",   # mixed
        "VoidBox{" + "CTF{fake_flag_inside_here}" + "}",   # nested flag
    ]
    
    for pattern in test_patterns:
        stdout, stderr, rc = run_cmd(f"echo '{pattern}' | ./{binary}")
        print(f"  {pattern[:50]}... -> {stdout.strip()}")
    
    # Step 5: Look for comparison values in disassembly
    print(f"\n[5] Looking for hash targets in disassembly...")
    
    try:
        with open("unpacked_disasm.txt", "r") as f:
            disasm_content = f.read()
        
        # Find immediate values that could be hash targets
        immediates = re.findall(r'\$0x([0-9a-f]{4,})', disasm_content)
        unique_imms = sorted(set(imm for imm in immediates if len(imm) >= 4))
        
        print(f"[+] Found potential hash targets:")
        for imm in unique_imms[:20]:  # Show first 20
            print(f"    0x{imm}")
        
        # Look for data section references
        data_refs = re.findall(r'0x([0-9a-f]+)\(%rip\)', disasm_content)
        if data_refs:
            print(f"\n[+] Data section references:")
            for ref in set(data_refs)[:10]:
                print(f"    0x{ref}")
                
    except FileNotFoundError:
        print("[-] No disassembly file found")
    
    print(f"\n[6] Analysis complete!")
    print("="*50)
    print("Next steps:")
    print("1. Check unpacked_strings.txt for format hints") 
    print("2. Analyze unpacked_disasm.txt for validation logic")
    print("3. Implement hash functions based on disassembly")
    print("4. Brute force the 27-character content")

if __name__ == "__main__":
    main()
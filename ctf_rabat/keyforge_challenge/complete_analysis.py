#!/usr/bin/env python3
"""
Complete KeyForge Analysis Script
Run this and share the output files with me
"""
import subprocess
import os
import sys

def run_cmd(cmd, input_data=None):
    """Run a command and return output"""
    try:
        if input_data:
            result = subprocess.run(cmd, shell=True, input=input_data.encode(), 
                                  capture_output=True, timeout=5)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, 
                                  text=True, timeout=5)
        
        stdout = result.stdout.decode('utf-8', errors='ignore') if isinstance(result.stdout, bytes) else result.stdout
        stderr = result.stderr.decode('utf-8', errors='ignore') if isinstance(result.stderr, bytes) else result.stderr
        return stdout, stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def main():
    """Complete analysis"""
    
    print("KeyForge Complete Analysis")
    print("="*50)
    
    results = {}
    
    # Test 1: Format variations
    print("[1] Testing input formats...")
    format_tests = [
        ("VoidBox{test}", "VoidBox format"),
        ("DeepSec{test}", "DeepSec format"),
        ("CTF{test}", "CTF format"),
        ("flag{test}", "flag format"),
        ("test", "plain text"),
        ("AAAA-BBBB-CCCC-DDDD", "license key format"),
        ("VoidBox{}", "empty VoidBox"),
        ("DeepSec{}", "empty DeepSec"),
        ("VoidBox{a}", "single char"),
        ("DeepSec{a}", "single char DeepSec"),
        ("VoidBox{" + "a"*27 + "}", "VoidBox 27 chars"),
        ("DeepSec{" + "a"*27 + "}", "DeepSec 27 chars"),
    ]
    
    format_results = []
    for test_input, description in format_tests:
        stdout, stderr, rc = run_cmd("./KeyForge", test_input + "\n")
        result_line = f"{description:20} | {test_input:35} | RC:{rc} | {stdout.strip()}"
        format_results.append(result_line)
        print(f"  {result_line}")
    
    results["format_tests"] = format_results
    
    # Test 2: Extract strings
    print("\n[2] Extracting strings...")
    stdout, stderr, rc = run_cmd("strings KeyForge")
    if rc == 0:
        all_strings = stdout.split('\n')
        interesting_strings = []
        keywords = ['enter', 'license', 'key', 'valid', 'invalid', 'format', 'void', 
                   'deep', 'sec', 'flag', 'correct', 'wrong', 'success', 'fail']
        
        for s in all_strings:
            if any(kw in s.lower() for kw in keywords) and len(s.strip()) > 2:
                interesting_strings.append(s.strip())
        
        results["all_strings"] = all_strings
        results["interesting_strings"] = interesting_strings
        
        print(f"  Found {len(all_strings)} total strings")
        print(f"  Found {len(interesting_strings)} interesting strings:")
        for s in interesting_strings[:10]:
            print(f"    {s}")
    
    # Test 3: Get disassembly
    print("\n[3] Getting disassembly...")
    stdout, stderr, rc = run_cmd("objdump -d -M intel KeyForge")
    if rc == 0:
        results["disassembly"] = stdout
        lines = stdout.split('\n')
        print(f"  Generated {len(lines)} lines of disassembly")
        
        # Look for main function
        main_start = -1
        for i, line in enumerate(lines):
            if '<main>' in line:
                main_start = i
                break
        
        if main_start >= 0:
            main_lines = []
            for i in range(main_start, min(main_start + 100, len(lines))):
                if lines[i].strip() and not lines[i].startswith(' '):
                    if '<' in lines[i] and '>' in lines[i] and i > main_start:
                        break
                main_lines.append(lines[i])
            
            results["main_function"] = main_lines
            print(f"  Extracted {len(main_lines)} lines from main function")
    
    # Test 4: Data section
    print("\n[4] Analyzing data section...")
    stdout, stderr, rc = run_cmd("objdump -s -j .data KeyForge")
    if rc == 0:
        results["data_section"] = stdout
        print("  Extracted data section")
    
    # Test 5: File information
    print("\n[5] Getting file info...")
    stdout, stderr, rc = run_cmd("file KeyForge")
    if rc == 0:
        results["file_info"] = stdout.strip()
        print(f"  {stdout.strip()}")
    
    # Test 6: Check for UPX packing
    print("\n[6] Checking for packing...")
    stdout, stderr, rc = run_cmd("upx -t KeyForge")
    results["upx_test"] = f"RC: {rc}, STDOUT: {stdout}, STDERR: {stderr}"
    if rc == 0:
        print("  Binary might be UPX packed")
    else:
        print("  Binary doesn't appear to be UPX packed")
    
    # Save all results to files
    print(f"\n[7] Saving results to files...")
    
    # Save format test results
    with open("format_test_results.txt", "w") as f:
        f.write("KeyForge Format Test Results\n")
        f.write("="*50 + "\n\n")
        for line in format_results:
            f.write(line + "\n")
    
    # Save strings
    if "all_strings" in results:
        with open("all_strings.txt", "w") as f:
            for s in results["all_strings"]:
                f.write(s + "\n")
        
        with open("interesting_strings.txt", "w") as f:
            f.write("Interesting Strings from KeyForge\n")
            f.write("="*40 + "\n\n")
            for s in results["interesting_strings"]:
                f.write(s + "\n")
    
    # Save disassembly
    if "disassembly" in results:
        with open("full_disassembly.txt", "w") as f:
            f.write(results["disassembly"])
    
    # Save main function
    if "main_function" in results:
        with open("main_function.txt", "w") as f:
            f.write("Main Function Disassembly\n")
            f.write("="*30 + "\n\n")
            for line in results["main_function"]:
                f.write(line + "\n")
    
    # Save data section
    if "data_section" in results:
        with open("data_section.txt", "w") as f:
            f.write(results["data_section"])
    
    # Save summary
    with open("analysis_summary.txt", "w") as f:
        f.write("KeyForge Analysis Summary\n")
        f.write("="*30 + "\n\n")
        
        f.write("File Info:\n")
        if "file_info" in results:
            f.write(f"  {results['file_info']}\n\n")
        
        f.write("UPX Test:\n")
        f.write(f"  {results['upx_test']}\n\n")
        
        f.write("Format Test Results:\n")
        for line in format_results:
            f.write(f"  {line}\n")
        
        if "interesting_strings" in results:
            f.write(f"\nInteresting Strings ({len(results['interesting_strings'])}):\n")
            for s in results["interesting_strings"]:
                f.write(f"  {s}\n")
    
    print("\nAnalysis Complete!")
    print("="*50)
    print("Files created:")
    print("- analysis_summary.txt (overview)")
    print("- format_test_results.txt (input format tests)")  
    print("- interesting_strings.txt (relevant strings)")
    print("- main_function.txt (main function disassembly)")
    print("- full_disassembly.txt (complete disassembly)")
    print("- data_section.txt (data section dump)")
    print("\nRun this script and share the analysis_summary.txt file!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Advanced KeyForge Reverse Engineering
Extract validation functions and implement hash cracking
"""
import subprocess
import re
import itertools
import string

def test_flag(content_27):
    """Test a 27-character content"""
    flag = f"VoidBox{{{content_27}}}"
    try:
        result = subprocess.run(['./KeyForge'], input=flag.encode() + b'\n',
                              capture_output=True, timeout=2)
        output = result.stdout.decode('utf-8', errors='ignore').strip()
        return output, result.returncode
    except:
        return "ERROR", -1

def extract_validation_hints():
    """Try to extract validation hints using different approaches"""
    print("[*] Analyzing binary for validation clues...")
    
    # Method 1: Check if binary has obvious strings after running
    print("\n[1] Testing edge cases to find validation boundaries...")
    
    # Test different lengths to confirm exactly 27 is required
    for length in [26, 27, 28]:
        test_content = "a" * length
        output, rc = test_flag(test_content)
        print(f"  Length {length:2}: {output}")
    
    # Method 2: Test character set restrictions
    print("\n[2] Testing character set restrictions...")
    
    char_sets = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase, 
        "digits": string.digits,
        "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?",
        "mixed": string.ascii_letters + string.digits + "_"
    }
    
    for name, charset in char_sets.items():
        if len(charset) >= 27:
            test_content = charset[:27]
            output, rc = test_flag(test_content)
            print(f"  {name:10}: {output}")
    
    # Method 3: Look for patterns in common CTF formats
    print("\n[3] Testing CTF-specific patterns...")
    
    ctf_patterns = [
        # Based on tetouan challenge structure, try similar patterns
        "wh0_s41d_y0" + "a" * 16,           # Similar to tetouan start
        "a" * 11 + "ahhrmi" + "a" * 10,     # Similar to tetouan middle  
        "a" * 17 + "ri_hgsklra",            # Similar to tetouan end
        
        # Common CTF flag content
        "ctf{this_is_the_flag_here}",       # 27 chars
        "flag{you_solved_the_puzzle}",      # 28 chars - test anyway
        "welcome_to_rabat_ctf_finals",      # 28 chars
        "congratulations_you_won_it",       # 27 chars
        
        # Hash-like patterns (might be expected hash result)
        "deadbeef" * 3 + "abc",             # 27 chars
        "1234567890abcdef" + "ghijklmno",   # 27 chars
        
        # Based on VoidBox theme
        "void_box_contains_the_flag",       # 27 chars
        "empty_void_filled_with_win",       # 27 chars
    ]
    
    for pattern in ctf_patterns:
        if len(pattern) <= 28:  # Test even slightly wrong lengths
            output, rc = test_flag(pattern[:27] if len(pattern) > 27 else pattern.ljust(27, 'x'))
            print(f"  {pattern[:25]:25}: {output}")
    
    return None

def brute_force_short_sections():
    """Try to brute force shorter sections that might be validated separately"""
    print("\n[4] Testing if validation is done in sections...")
    
    # Based on tetouan challenge, validation might be in parts
    # Try systematic approach for first few characters
    
    print("  Testing first 3 characters systematically...")
    
    # Common 3-char prefixes in CTF flags
    prefixes_3 = ["CTF", "ctf", "flag", "key", "win", "you", "got", "voi", "box", "sec", "pwn"]
    
    for prefix in prefixes_3:
        test_content = prefix + "a" * 24
        output, rc = test_flag(test_content)
        print(f"    {prefix}{'a'*24}: {output}")
        
        # If we get a different response, this might be correct
        if "validation failed" not in output.lower() and "invalid format" not in output.lower():
            print(f"    ^ Different response! Might be onto something...")

def analyze_timing():
    """Check if timing analysis reveals validation structure"""
    print("\n[5] Timing analysis...")
    
    import time
    
    # Test if different inputs take different time (indicating validation depth)
    test_cases = [
        "a" * 27,                           # All same
        "VoidBox{test}" + "a" * 14,         # Nested format
        string.ascii_lowercase[:27],         # Sequential
        "the_quick_brown_fox_jumps_",       # English text
    ]
    
    for test_content in test_cases:
        if len(test_content) == 27:
            start_time = time.time()
            output, rc = test_flag(test_content)
            elapsed = time.time() - start_time
            print(f"  {test_content[:20]:20}... : {elapsed:.4f}s - {output}")

def main():
    print("Advanced KeyForge Reverse Engineering")
    print("="*60)
    
    # Run all analysis methods
    extract_validation_hints()
    brute_force_short_sections()
    analyze_timing()
    
    print(f"\n[6] Summary and next steps:")
    print("- Binary requires exactly 27 characters in VoidBox{} format")
    print("- All tested patterns give 'License validation failed'") 
    print("- Need to reverse engineer the actual validation algorithm")
    print("\nRecommended approach:")
    print("1. Use gdb to debug the binary during validation")
    print("2. Analyze assembly code for hash functions") 
    print("3. Implement hash functions and brute force")
    print("4. Or try more targeted wordlist attacks")

if __name__ == "__main__":
    main()
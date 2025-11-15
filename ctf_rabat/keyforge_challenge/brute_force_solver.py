#!/usr/bin/env python3
"""
KeyForge Brute Force Solver
Since simple guesses didn't work, try more systematic approach
"""
import subprocess
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
import time

def test_flag_content(content_27):
    """Test a 27-character content in VoidBox format"""
    if len(content_27) != 27:
        return f"Wrong length: {len(content_27)}", -1
    
    flag = f"VoidBox{{{content_27}}}"
    try:
        result = subprocess.run(['./KeyForge'], input=flag.encode() + b'\n',
                              capture_output=True, timeout=2)
        output = result.stdout.decode('utf-8', errors='ignore').strip()
        return output, result.returncode
    except Exception as e:
        return f"ERROR: {e}", -1

def test_wordlist_approach():
    """Try common words and phrases"""
    print("[1] Testing wordlist approach...")
    
    # Common CTF flag components
    words = [
        "welcome", "congratulations", "you", "found", "the", "flag", "here",
        "ctf", "challenge", "solved", "complete", "success", "winner",
        "rabat", "finals", "keyforge", "reverse", "engineering", "binary",
        "void", "box", "empty", "full", "hidden", "secret", "key", "license",
        "validation", "passed", "correct", "right", "answer", "solution"
    ]
    
    # Try single words padded to 27 chars
    for word in words:
        if len(word) <= 27:
            # Pad with underscores
            padded = word + "_" * (27 - len(word))
            output, rc = test_flag_content(padded)
            print(f"  {padded}: {output}")
            
            if is_success(output):
                return f"VoidBox{{{padded}}}"
    
    # Try combinations of words
    print("  Testing word combinations...")
    for w1, w2 in itertools.combinations(words[:10], 2):
        combined = f"{w1}_{w2}"
        if len(combined) <= 27:
            padded = combined + "_" * (27 - len(combined))
            output, rc = test_flag_content(padded)
            if is_success(output):
                return f"VoidBox{{{padded}}}"
    
    return None

def test_format_variations():
    """Test different format approaches"""
    print("\n[2] Testing format variations...")
    
    # Maybe it expects a different internal format
    internal_formats = [
        "CTF{this_is_the_real_flag}",           # CTF inside VoidBox
        "FLAG{hidden_inside_here__}",           # FLAG inside VoidBox  
        "flag{you_found_it_congrats}",          # lowercase flag
        "{this_is_just_curly_braces}",          # Just braces
        "DeepSec{wh0_s41d_y0ahhrmi}",          # Similar to tetouan (truncated)
        "VOIDBOX_CONTAINS_THE_KEY_1",           # No braces at all
        "keyforge_license_validated",           # Simple description
        "reverse_engineering_success",          # What you did
        "congratulations_you_solved",           # Success message
    ]
    
    for fmt in internal_formats:
        if len(fmt) <= 27:
            padded = fmt.ljust(27, '_')
            output, rc = test_flag_content(padded)
            print(f"  {padded}: {output}")
            
            if is_success(output):
                return f"VoidBox{{{padded}}}"
    
    return None

def test_character_patterns():
    """Test systematic character patterns"""
    print("\n[3] Testing character patterns...")
    
    patterns = [
        # Repeating patterns
        "abc" * 9,                              # abcabcabc... (27 chars)
        "123" * 9,                              # 123123123...
        "xyz" * 9,                              # xyzxyzxyz...
        
        # Sequential patterns  
        string.ascii_lowercase[:27],             # abcdefghijklmnopqrstuvwxyz + a
        string.ascii_uppercase[:27],             # ABCDEFGHIJKLMNOPQRSTUVWXYZ + A
        string.digits * 3,                      # 012345678901234567890123456
        
        # Mixed patterns
        "aA1" * 9,                              # aA1aA1aA1...
        "flag_" + "x" * 22,                     # flag_ + padding
        "key_" + "0" * 23,                      # key_ + padding
        
        # Hash-like
        "deadbeef" * 3 + "abc",                 # Hex-like
        "ff00ff00" * 3 + "abc",                 # More hex-like
    ]
    
    for pattern in patterns:
        if len(pattern) == 27:
            output, rc = test_flag_content(pattern)
            print(f"  {pattern}: {output}")
            
            if is_success(output):
                return f"VoidBox{{{pattern}}}"
    
    return None

def test_instruction_variations():
    """Test variations of the instruction example"""
    print("\n[4] Testing instruction variations...")
    
    original = "Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard"
    
    # Different substrings of the original
    variations = []
    
    # Sliding window of 27 characters
    for i in range(len(original) - 26):
        substr = original[i:i+27]
        variations.append(substr)
    
    # Common modifications
    variations.extend([
        "Welcome_To_our_Hummble_Ctf",          # First part
        "did_you_really_think_this_",          # Middle part  
        "you_really_think_this_was_",          # Different middle
        "think_this_was_hard_right",           # End part modified
        "WELCOME_TO_OUR_HUMMBLE_CTF",          # Uppercase
        "welcome_to_our_hummble_ctf",          # Lowercase
    ])
    
    for var in variations:
        if len(var) == 27:
            output, rc = test_flag_content(var)
            print(f"  {var}: {output}")
            
            if is_success(output):
                return f"VoidBox{{{var}}}"
    
    return None

def is_success(output):
    """Check if output indicates success"""
    success_indicators = [
        'license valid', 'valid!', 'correct', 'success', 'congratulations',
        'well done', 'you win', 'flag accepted', 'access granted'
    ]
    
    return any(indicator in output.lower() for indicator in success_indicators)

def main():
    print("KeyForge Advanced Brute Force Solver")
    print("="*60)
    print("Systematically testing different approaches...\n")
    
    approaches = [
        test_wordlist_approach,
        test_format_variations, 
        test_character_patterns,
        test_instruction_variations
    ]
    
    for approach in approaches:
        try:
            result = approach()
            if result:
                print(f"\n{'='*60}")
                print(f"SUCCESS! FOUND FLAG: {result}")
                print(f"{'='*60}")
                return result
        except Exception as e:
            print(f"Error in approach: {e}")
    
    print(f"\n{'='*60}")
    print("No flag found with systematic approaches.")
    print("The challenge likely requires:")
    print("1. Hash function reverse engineering")
    print("2. Binary analysis with gdb/radare2")  
    print("3. Custom algorithm implementation")
    print("4. Or hidden hints not yet discovered")
    print(f"{'='*60}")
    
    return None

if __name__ == "__main__":
    main()
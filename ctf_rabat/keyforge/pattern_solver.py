#!/usr/bin/env python3
"""
KeyForge Pattern Solver
Since we know VoidBox{27 chars} works, let's systematically find the right content
"""
import subprocess
import itertools
import string
import sys

def test_flag(content_27):
    """Test a 27-character content in VoidBox format"""
    flag = f"VoidBox{{{content_27}}}"
    try:
        result = subprocess.run(['./KeyForge'], input=flag.encode() + b'\n',
                              capture_output=True, timeout=2)
        output = result.stdout.decode('utf-8', errors='ignore').strip()
        return output, result.returncode
    except:
        return "ERROR", -1

def main():
    print("KeyForge Pattern Solver")
    print("="*50)
    print("We know format is VoidBox{27 characters}")
    print("Looking for the correct 27-character content...\n")
    
    # Step 1: Test common patterns
    print("[1] Testing common CTF patterns...")
    
    common_patterns = [
        # Standard CTF content patterns
        "welcome_to_our_ctf_challenge",  # 27 chars
        "WELCOME_TO_OUR_CTF_CHALLENGE",
        "abcdefghijklmnopqrstuvwxyz1",   # alphabet + 1
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ1", 
        "123456789012345678901234567",   # all numbers
        "ctf_challenge_solved_here_1",   
        "flag_content_goes_here_123",
        "reverse_engineering_is_fun",
        "this_is_the_correct_answer",
        "you_found_the_hidden_secret",
        
        # Variations based on instructions 
        "Welcome_To_our_Hummble_Ctf",   # Part of example (27 chars)
        "did_you_really_think_this_",
        "was_hard_congratulations_1", 
        
        # Leetspeak variations
        "w3lc0m3_t0_0ur_ctf_ch4ll3ng3",  # 27 chars with numbers
        "y0u_f0und_th3_h1dd3n_s3cr3t",
        "r3v3rs3_3ng1n33r1ng_1s_fun",
        
        # Common flag formats inside
        "CTF{this_is_the_real_flag}",
        "FLAG{hidden_inside_voidbox}",
        
        # Hex/Base64-like
        "deadbeefcafebabe1234567890a",   # 27 hex chars
        "DEADBEEFCAFEBABE1234567890A",
    ]
    
    for pattern in common_patterns:
        if len(pattern) == 27:
            output, rc = test_flag(pattern)
            print(f"  {pattern[:30]:35} -> {output}")
            
            # Check for success indicators
            if "valid" in output.lower() or "correct" in output.lower() or "success" in output.lower():
                print(f"\n*** FOUND FLAG: VoidBox{{{pattern}}} ***")
                return f"VoidBox{{{pattern}}}"
    
    # Step 2: Try variations of the example string
    print(f"\n[2] Testing variations of the instruction example...")
    
    # The instruction example was too long, but parts might work
    example = "Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard"
    
    # Try different 27-char substrings
    for i in range(len(example) - 26):
        substr = example[i:i+27]
        if len(substr) == 27:
            output, rc = test_flag(substr)
            print(f"  {substr[:35]:35} -> {output}")
            
            if "valid" in output.lower() or "correct" in output.lower():
                print(f"\n*** FOUND FLAG: VoidBox{{{substr}}} ***")
                return f"VoidBox{{{substr}}}"
    
    # Step 3: Try alphabet-based patterns
    print(f"\n[3] Testing alphabet and number combinations...")
    
    alphabet_patterns = [
        string.ascii_lowercase[:27],                    # abcd...
        string.ascii_uppercase[:27],                    # ABCD...
        (string.ascii_lowercase + "123")[:27],          # abc...xyz123
        (string.ascii_uppercase + "123")[:27],          # ABC...XYZ123
        ("123" + string.ascii_lowercase)[:27],          # 123abc...
        (string.digits * 3)[:27],                       # 012301230123...
    ]
    
    for pattern in alphabet_patterns:
        if len(pattern) == 27:
            output, rc = test_flag(pattern)
            print(f"  {pattern[:35]:35} -> {output}")
            
            if "valid" in output.lower() or "correct" in output.lower():
                print(f"\n*** FOUND FLAG: VoidBox{{{pattern}}} ***")
                return f"VoidBox{{{pattern}}}"
    
    # Step 4: Try common words/phrases
    print(f"\n[4] Testing common words and phrases...")
    
    word_patterns = [
        "keyforge" + "_" * 19,                          # keyforge + padding
        "license_key_validation_ok",                     # 26 + 1 padding
        "congratulations_you_won_1",                     # 27 chars
        "challenge_completed_here_1",                    # 27 chars  
        "reverse_engineer_success_1",                    # 27 chars
        "binary_analysis_complete_1",                    # 27 chars
    ]
    
    for pattern in word_patterns:
        if len(pattern) == 27:
            output, rc = test_flag(pattern)
            print(f"  {pattern[:35]:35} -> {output}")
            
            if "valid" in output.lower() or "correct" in output.lower():
                print(f"\n*** FOUND FLAG: VoidBox{{{pattern}}} ***")
                return f"VoidBox{{{pattern}}}"
    
    print(f"\n[5] No obvious pattern found.")
    print("Need to analyze disassembly for hash validation functions.")
    print("The binary likely validates the 27 chars using hash functions.")
    
    return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n{'='*60}")
        print(f"SUCCESS! FLAG: {result}")
        print(f"{'='*60}")
    else:
        print(f"\nNo flag found with common patterns.")
        print(f"Next: Need to reverse engineer the hash validation.")

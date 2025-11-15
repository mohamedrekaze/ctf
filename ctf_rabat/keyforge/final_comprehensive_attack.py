#!/usr/bin/env python3
"""
KeyForge Final Attack - Comprehensive Solution
Last attempt using all gathered intelligence
"""
import subprocess
import string
import itertools

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

def test_meta_solutions():
    """Test meta-level solutions based on CTF psychology"""
    print("[FINAL] Testing meta-level solutions...")
    
    # Sometimes the flag is literally describing what you need to do
    meta_flags = [
        "read_the_source_code_please",      # 27 chars
        "this_is_not_the_real_flag_",       # 27 chars
        "check_other_files_for_clues",      # 28 chars - trim
        "the_flag_is_in_plain_sight",       # 27 chars
        "look_harder_at_the_binary_",       # 27 chars
        "disassemble_and_understand",       # 27 chars
        "gdb_will_reveal_the_secret",       # 27 chars
        "hash_functions_hold_the_key",      # 28 chars - trim
        "brute_force_wont_work_here",       # 27 chars
        "reverse_engineer_the_logic",       # 27 chars
        "its_simpler_than_you_think",       # 27 chars
        "overthinking_this_problem_",       # 27 chars
        "back_to_basics_read_manual",       # 27 chars
    ]
    
    for flag in meta_flags:
        # Ensure exactly 27 chars
        if len(flag) > 27:
            flag = flag[:27]
        elif len(flag) < 27:
            flag = flag + "_" * (27 - len(flag))
        
        output, rc = test_flag_content(flag)
        print(f"  {flag}: {output}")
        
        if is_success(output):
            return f"VoidBox{{{flag}}}"
    
    return None

def test_numerical_patterns():
    """Test patterns that might be hash targets or mathematical"""
    print("\n[FINAL] Testing numerical and hash-like patterns...")
    
    # Common hash-like values that might be expected
    hash_patterns = [
        "deadbeef" * 3 + "123",             # 27 chars
        "cafebabe" * 3 + "123",             # 27 chars  
        "1337133713371337133713371",        # 1337 repeated
        "42424242424242424242424242",       # 42 repeated (answer to everything)
        "0123456789abcdef0123456789",       # hex sequence
        "fedcba9876543210fedcba9876",       # reverse hex
        "aaaaaaaaaaaaaaaaaaaaaaaaa",        # All a's (might bypass validation)
        "zzzzzzzzzzzzzzzzzzzzzzzzz",        # All z's
        "00000000000000000000000000",       # All zeros
        "11111111111111111111111111",       # All ones
        "ffffffffffffffffffffffffff",       # All f's (hex)
    ]
    
    for pattern in hash_patterns:
        if len(pattern) == 27:
            output, rc = test_flag_content(pattern)
            print(f"  {pattern}: {output}")
            
            if is_success(output):
                return f"VoidBox{{{pattern}}}"
    
    return None

def test_instruction_forensics():
    """Deep analysis of the instruction example"""
    print("\n[FINAL] Deep analysis of instruction text...")
    
    original = "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}"
    content = "Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard"
    
    print(f"Original instruction length: {len(content)} chars")
    print(f"Need exactly 27 chars")
    
    # Try every possible 27-char substring
    substrings = []
    for i in range(len(content) - 26):
        substr = content[i:i+27]
        substrings.append(substr)
    
    print(f"Testing {len(substrings)} substrings from instruction...")
    
    for i, substr in enumerate(substrings[:10]):  # Test first 10
        output, rc = test_flag_content(substr)
        print(f"  [{i:2}] {substr}: {output}")
        
        if is_success(output):
            return f"VoidBox{{{substr}}}"
    
    # Try modifications of key parts
    modifications = [
        "Welcome_To_our_Hummble_C",         # Exact truncation
        "elcome_To_our_Hummble_Ct",         # Shifted by 1
        "lcome_To_our_Hummble_Ctf",         # Shifted by 2
        "WELCOME_TO_OUR_HUMMBLE_C",         # Uppercase
        "welcome_to_our_hummble_c",         # Lowercase
        "Welcome_To_our_Humble_Ct",         # Fixed typo
    ]
    
    for mod in modifications:
        if len(mod) == 27:
            output, rc = test_flag_content(mod)
            print(f"  MOD: {mod}: {output}")
            
            if is_success(output):
                return f"VoidBox{{{mod}}}"
    
    return None

def test_challenge_context():
    """Test patterns based on challenge context"""
    print("\n[FINAL] Testing challenge-specific patterns...")
    
    context_flags = [
        # Rabat/Morocco themed
        "rabat_morocco_ctf_finals_20",      # 25 chars + 25
        "morocco_rabat_keyforge_cha",       # 27 chars
        "finals_in_rabat_morocco_1_",       # 27 chars
        
        # KeyForge themed  
        "keyforge_binary_cracked_ok",       # 27 chars
        "license_key_validation_ok_",       # 27 chars
        "keyforge_reverse_engineered",      # 28 chars - trim
        
        # Success themed
        "challenge_complete_well_do",       # 27 chars
        "congratulations_champion_1",       # 27 chars
        "you_are_the_ctf_master_no",        # 27 chars
        
        # Date/event themed
        "november_2025_rabat_finals",       # 27 chars
        "ctf_finals_november_fifteen",      # 28 chars - trim
    ]
    
    for flag in context_flags:
        # Ensure exactly 27 chars
        if len(flag) > 27:
            flag = flag[:27]
        elif len(flag) < 27:
            flag = flag + "_" * (27 - len(flag))
        
        output, rc = test_flag_content(flag)
        print(f"  {flag}: {output}")
        
        if is_success(output):
            return f"VoidBox{{{flag}}}"
    
    return None

def is_success(output):
    """Check if output indicates success"""
    success_indicators = [
        'license valid', 'valid!', 'correct', 'success', 'congratulations',
        'well done', 'you win', 'flag accepted', 'access granted', 'welcome',
        'authenticated', 'authorized', 'passed', 'cracked'
    ]
    
    return any(indicator in output.lower() for indicator in success_indicators)

def main():
    print("KeyForge FINAL COMPREHENSIVE ATTACK")
    print("="*60)
    print("Last systematic attempt before deep reverse engineering\n")
    
    final_approaches = [
        test_meta_solutions,
        test_numerical_patterns,
        test_instruction_forensics,
        test_challenge_context
    ]
    
    for approach in final_approaches:
        try:
            result = approach()
            if result:
                print(f"\n{'='*60}")
                print(f"SUCCESS! FOUND FLAG: {result}")
                print(f"{'='*60}")
                
                # Verify the flag
                content = result[8:-1]  # Extract content between VoidBox{ and }
                output, rc = test_flag_content(content)
                print(f"VERIFICATION: {output}")
                return result
        except Exception as e:
            print(f"Error in approach: {e}")
    
    print(f"\n{'='*60}")
    print("FINAL ANALYSIS COMPLETE")
    print("="*60)
    print("No flag found with comprehensive systematic approaches.")
    print("This challenge requires one of:")
    print("1. Deep binary reverse engineering (disassembly analysis)")
    print("2. Hash function extraction and custom implementation")  
    print("3. Dynamic analysis with gdb/radare2")
    print("4. Additional challenge files or hints not yet found")
    print("5. Specific domain knowledge about the CTF context")
    print()
    print("The binary uses sophisticated validation beyond simple pattern matching.")
    print("Recommend using gdb to step through validation functions.")
    print("="*60)
    
    return None

if __name__ == "__main__":
    main()
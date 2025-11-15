#!/usr/bin/env python3
"""
Hash-based approach for KeyForge
Similar to tetouan challenge structure
"""

def test_flag_content(content_27):
    """Test a 27-character content in VoidBox format"""
    import subprocess
    
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

def main():
    print("Hash-based KeyForge Solver")
    print("="*40)
    
    # Based on tetouan challenge pattern: sections validated separately
    # Try patterns similar to: "wh0_s41d_y0" + "ahhrmi" + "ri_hgsklra"
    
    print("Testing tetouan-style patterns...")
    
    # Common leet speak patterns (11 + 6 + 10 = 27)
    patterns_11_6_10 = [
        ("wh0_s41d_y0", "ahhrmi", "ri_hgsklra"),  # Original tetouan
        ("r4b4t_ctf_f", "1n4ls_", "k3yf0rg3_1"),  # Rabat CTF finals  
        ("v01d_b0x_1s", "_3mpty_", "n0w_fu11_1"), # VoidBox theme
        ("k3y_f0rg3_1", "s_th3_", "4nsw3r_h3r"), # KeyForge theme
        ("h4ck_th3_b1", "n4ry_", "4nd_w1n_17"), # Hacking theme
        ("y0u_f0und_1t", "_h3r3_", "1n_th3_v01d"), # Success theme
    ]
    
    for p1, p2, p3 in patterns_11_6_10:
        if len(p1) == 11 and len(p2) == 6 and len(p3) == 10:
            content = p1 + p2 + p3
            output, rc = test_flag_content(content)
            print(f"  {content}: {output}")
    
    print("\nTesting other length combinations...")
    
    # Try different length splits that sum to 27
    length_combinations = [
        (9, 9, 9),   # Equal thirds
        (13, 7, 7),  # Different split
        (5, 11, 11), # Another split
        (27,),       # Single piece
    ]
    
    base_parts = [
        "rabat", "ctf", "finals", "keyforge", "void", "box", "flag", 
        "key", "license", "valid", "success", "win", "solved", "correct"
    ]
    
    import itertools
    
    for lengths in length_combinations[:2]:  # Test first 2 combinations
        if len(lengths) == 3:
            l1, l2, l3 = lengths
            for w1, w2, w3 in itertools.combinations(base_parts, 3):
                p1 = (w1 + "_" * l1)[:l1]
                p2 = (w2 + "_" * l2)[:l2] 
                p3 = (w3 + "_" * l3)[:l3]
                
                content = p1 + p2 + p3
                if len(content) == 27:
                    output, rc = test_flag_content(content)
                    if "validation failed" not in output.lower():
                        print(f"  {content}: {output}")
    
    # Try the most likely single-word approaches
    print("\nTesting single coherent phrases...")
    
    coherent_27_chars = [
        "welcome_to_rabat_ctf_finals",  # 28 chars - trim to 27
        "congratulations_you_solved",   # 26 chars - pad to 27  
        "keyforge_challenge_complete",  # 28 chars - trim to 27
        "reverse_engineering_master",   # 27 chars exactly
        "binary_analysis_successful",   # 27 chars exactly
        "license_validation_passed",    # 27 chars exactly
        "you_cracked_the_algorithm_",   # 27 chars exactly
        "void_box_now_contains_flag",   # 27 chars exactly
        "rabat_morocco_ctf_champion",   # 27 chars exactly
    ]
    
    for phrase in coherent_27_chars:
        # Adjust to exactly 27 characters
        if len(phrase) > 27:
            phrase = phrase[:27]
        elif len(phrase) < 27:
            phrase = phrase + "_" * (27 - len(phrase))
        
        output, rc = test_flag_content(phrase)
        print(f"  {phrase}: {output}")
        
        # Check for success
        if any(word in output.lower() for word in ['valid!', 'success', 'correct', 'congratulations']):
            print(f"\nSUCCESS! FLAG: VoidBox{{{phrase}}}")
            return f"VoidBox{{{phrase}}}"
    
    print("\nNo obvious pattern found.")
    print("Recommendation: Use gdb to analyze validation functions")

if __name__ == "__main__":
    main()
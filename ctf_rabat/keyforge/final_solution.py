#!/usr/bin/env python3
"""
KeyForge Final Solution Attempt
Based on analysis, try the most likely solutions
"""
import subprocess

def test_flag(content):
    """Test a flag content"""
    if not content.startswith("VoidBox{") or not content.endswith("}"):
        content = f"VoidBox{{{content}}}"
    
    try:
        result = subprocess.run(['./KeyForge'], input=content.encode() + b'\n',
                              capture_output=True, timeout=2)
        output = result.stdout.decode('utf-8', errors='ignore').strip()
        return output, result.returncode
    except:
        return "ERROR", -1

def main():
    print("KeyForge Final Solution Attempts")
    print("="*50)
    
    # Based on the instruction example and common CTF patterns
    high_probability_flags = [
        # Most likely based on instructions
        "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}",
        
        # Corrected versions (fixing typos)
        "VoidBox{Welcome_To_our_Humble_Ctf_did_you_really_think_this_was_hard}",
        
        # Shortened versions (27 chars)
        "VoidBox{Welcome_To_our_Hummble_C}",
        "VoidBox{did_you_really_think_this}",
        "VoidBox{you_really_think_this_was}",
        
        # Based on challenge theme
        "VoidBox{rabat_ctf_finals_2025_key}",
        "VoidBox{keyforge_challenge_solved}",
        "VoidBox{reverse_engineering_master}",
        
        # Common CTF solutions  
        "VoidBox{this_is_the_correct_flag}",
        "VoidBox{congratulations_you_won_}",
        "VoidBox{ctf_challenge_complete___}",
        
        # Tetouan-style (similar structure)
        "VoidBox{wh0_s41d_y0ahhrmiri_hgskl}",
        "VoidBox{r4b4t_ctf_f1n4ls_k3yf0rg3}",
        
        # Simple patterns that might work
        "VoidBox{abcdefghijklmnopqrstuvwxyz1}",
        "VoidBox{ABCDEFGHIJKLMNOPQRSTUVWXYZ1}",
        "VoidBox{flag_goes_here_in_this_box}",
    ]
    
    print("Testing high-probability flags:")
    print("-" * 50)
    
    for flag in high_probability_flags:
        output, rc = test_flag(flag)
        print(f"{flag[:45]:45}... -> {output}")
        
        # Check for success
        if any(word in output.lower() for word in ['valid!', 'success', 'correct', 'congratulations', 'well done']):
            print(f"\n{'='*60}")
            print(f"SUCCESS! FOUND FLAG: {flag}")
            print(f"{'='*60}")
            return flag
            
        elif "validation failed" not in output.lower() and "invalid format" not in output.lower() and output != "ERROR":
            print(f"  ^ Different response - investigate further!")
    
    print(f"\nNo obvious flag found.")
    print(f"The challenge likely requires:")
    print(f"1. Deeper reverse engineering of validation functions")
    print(f"2. Hash cracking based on assembly analysis") 
    print(f"3. Or specific knowledge about the CTF/challenge context")
    
    return None

if __name__ == "__main__":
    result = main()
    if not result:
        print(f"\nNext steps:")
        print(f"- Run: python3 advanced_analysis.py")
        print(f"- Analyze assembly code manually") 
        print(f"- Use gdb for dynamic analysis")
        print(f"- Check if challenge has additional hints/files")
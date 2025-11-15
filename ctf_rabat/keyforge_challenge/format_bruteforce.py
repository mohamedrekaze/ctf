#!/usr/bin/env python3
"""
KeyForge Format Brute Forcer
Since we know VoidBox{...} gives "Invalid format", try other formats
"""
import subprocess
import itertools
import string

BINARY = '/workspaces/ctf/ctf_rabat/keyforge/KeyForge'

def test_input(inp):
    """Test an input and return the response"""
    try:
        result = subprocess.run([BINARY], input=inp.encode() + b'\n',
                              capture_output=True, timeout=2)
        return result.stdout.decode('utf-8', errors='ignore').strip()
    except:
        return "ERROR"

def main():
    """Try different formats to find the correct one"""
    
    print("KeyForge Format Discovery")
    print("="*50)
    
    # We know VoidBox{...} gives "Invalid format"
    # Let's try other common CTF flag formats
    
    test_formats = [
        # Different prefixes
        "flag{test}",
        "FLAG{test}", 
        "CTF{test}",
        "VOIDBOX{test}",
        "voidbox{test}",
        "DeepSec{test}",  # From tetouan challenge
        
        # License key formats
        "XXXX-XXXX-XXXX-XXXX",
        "AAAA-BBBB-CCCC-DDDD",
        "1234-5678-9ABC-DEF0",
        
        # Simple strings
        "test",
        "license",
        "key123",
        
        # Different bracket styles
        "VoidBox[test]",
        "VoidBox(test)",
        "VoidBox<test>",
        
        # No brackets
        "VoidBox_test",
        "VoidBox test",
        
        # Different lengths
        "VoidBox{a}",
        "VoidBox{ab}",
        "VoidBox{abc}",
        "VoidBox{abcd}",
        "VoidBox{" + "a"*10 + "}",
        "VoidBox{" + "a"*20 + "}",
        "VoidBox{" + "a"*27 + "}",  # Same as tetouan
        "VoidBox{" + "a"*32 + "}",
        
    ]
    
    print("Testing different formats:")
    print("-" * 50)
    
    for fmt in test_formats:
        response = test_input(fmt)
        print(f"{fmt:35} -> {response}")
        
        # Look for success indicators
        if any(word in response.lower() for word in ['valid', 'correct', 'success', 'congratulations']):
            print(f"\n*** POTENTIAL SUCCESS: {fmt} ***")
        elif response != "Invalid format." and response != "ERROR":
            print(f"    ^ Different response!")
    
    print("\n" + "="*50)
    print("Analysis complete.")
    print("\nNext steps if no success:")
    print("1. Check disassembly for exact format requirements")  
    print("2. Look for hash validation functions")
    print("3. Reverse engineer the validation algorithm")

if __name__ == "__main__":
    main()
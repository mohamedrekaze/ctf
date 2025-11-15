#!/usr/bin/env python3
"""
Verify the found flag and test variations
"""
import subprocess

def test_flag_content(content_27):
    """Test a 27-character content in VoidBox format"""
    flag = f"VoidBox{{{content_27}}}"
    print(f"Testing: {flag}")
    
    try:
        result = subprocess.run(['./KeyForge'], input=flag.encode() + b'\n',
                              capture_output=True, timeout=2)
        output = result.stdout.decode('utf-8', errors='ignore').strip()
        return output, result.returncode
    except Exception as e:
        return f"ERROR: {e}", -1

def main():
    print("VERIFYING FOUND FLAG")
    print("="*50)
    
    # The content that showed "License valid!"
    found_content = "wh0_s41d_y0ahhrmiri_hgsklra"
    
    print(f"Found content: {found_content}")
    print(f"Length: {len(found_content)} chars")
    print()
    
    output, rc = test_flag_content(found_content)
    print(f"Output: {output}")
    print(f"Return code: {rc}")
    
    if "License valid!" in output:
        print("\n" + "="*50)
        print("SUCCESS! This is the correct flag!")
        print(f"FLAG: VoidBox{{{found_content}}}")
        print("="*50)
    else:
        print("\nFlag verification failed. Checking variations...")
        
        # Test some variations just in case
        variations = [
            found_content.upper(),
            found_content.lower(),
            found_content.replace('0', 'o'),
            found_content.replace('1', 'l'),
        ]
        
        for var in variations:
            if len(var) == 27:
                output, rc = test_flag_content(var)
                print(f"  {var}: {output}")
                
                if "License valid!" in output:
                    print(f"\nSUCCESS with variation: VoidBox{{{var}}}")
                    break

if __name__ == "__main__":
    main()
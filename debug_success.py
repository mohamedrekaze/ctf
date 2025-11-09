#!/usr/bin/env python3
import socket
import re

HOST = '10.25.1.225'
PORT = 9999

def test_success_detection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(4096)
    s.sendall(b"DeepSec{a\n")
    response = s.recv(4096).decode()
    s.close()
    
    print("Response:")
    print(response)
    print("\nChecking conditions:")
    print(f"  '✅' in response: {'✅' in response}")
    print(f"  'CORRECT' in response.upper(): {'CORRECT' in response.upper()}")
    print(f"  'Access granted' in response: {'Access granted' in response}")
    print(f"  'SUCCESS' in response.upper(): {'SUCCESS' in response.upper()}")
    print(f"  'You got it' in response: {'You got it' in response}")
    print(f"  'congratulations' in response.lower(): {'congratulations' in response.lower()}")
    
    is_correct = ("✅" in response or "CORRECT" in response.upper() or 
                 "Access granted" in response or "SUCCESS" in response.upper() or
                 "You got it" in response or "congratulations" in response.lower())
    
    print(f"\nFinal is_correct: {is_correct}")

test_success_detection()

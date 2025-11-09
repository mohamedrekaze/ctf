#!/usr/bin/env python3
"""
Manual connection script - provide IP address
"""
import socket
import sys

# Get IP from command line or use default
if len(sys.argv) > 1:
    HOST = sys.argv[1]
else:
    HOST = input("Enter IP address for ctf.1337.ma: ")

PORT = 9999

print(f"Connecting to {HOST}:{PORT}...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    # Receive initial message
    response = s.recv(4096).decode()
    print("=" * 60)
    print("SERVER RESPONSE:")
    print(response)
    print("=" * 60)
    
    # Interactive mode
    print("\nEntering interactive mode. Type your input and press Enter.")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'quit':
            break
        
        s.sendall((user_input + '\n').encode())
        response = s.recv(4096).decode()
        print(response)
    
    s.close()
    
except Exception as e:
    print(f"Error: {e}")

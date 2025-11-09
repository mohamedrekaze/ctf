#!/usr/bin/env python3
import socket
import re

HOST = '10.25.1.225'
PORT = 9999

def test_flag(flag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(4096)  # Initial prompt
    s.sendall((flag + '\n').encode())
    response = s.recv(4096).decode()
    s.close()
    
    # Parse verification time
    server_time = 0.0
    if "Verification time:" in response:
        match = re.search(r'Verification time:\s*([\d.]+)s', response)
        if match:
            server_time = float(match.group(1))
    
    print(f"Flag: {flag}")
    print(f"Server time: {server_time}s")
    print(f"Response:\n{response}")
    print("="*60)
    return server_time

# Test a few flags
for flag in ["DeepSec{a", "DeepSec{b", "DeepSec{t", "DeepSec{x"]:
    test_flag(flag)

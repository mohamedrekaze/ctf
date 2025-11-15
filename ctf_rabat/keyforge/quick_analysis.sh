#!/bin/bash
# Quick analysis script

echo "=== KeyForge Analysis ==="
cd /workspaces/ctf/ctf_rabat/keyforge
chmod +x KeyForge

echo -e "\n[1] Testing format variations:"
echo "VoidBox{test}" | ./KeyForge 2>&1 | sed 's/^/  /'
echo "DeepSec{test}" | ./KeyForge 2>&1 | sed 's/^/  /'  
echo "test123" | ./KeyForge 2>&1 | sed 's/^/  /'

echo -e "\n[2] Extracting validation strings:"
strings KeyForge | grep -iE "(enter|license|key|valid|invalid|format|correct|wrong)" | head -10

echo -e "\n[3] Looking for format patterns in binary:"
strings KeyForge | grep -E "^[A-Za-z]{3,}\{.*\}$" | head -5

echo -e "\n[4] Checking for specific strings:"
strings KeyForge | grep -i void
strings KeyForge | grep -i box

echo -e "\n[5] Getting file info:"
file KeyForge

echo -e "\nDone. Check output above for clues."
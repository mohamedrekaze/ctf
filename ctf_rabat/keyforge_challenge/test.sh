#!/bin/bash
cd /workspaces/ctf/ctf_rabat/keyforge
chmod +x KeyForge

echo "Testing example flag from instructions..."
echo "VoidBox{Welcome_To_our_Hummble_Ctf_did_you_really_think_this_was_hard}" | ./KeyForge

echo ""
echo "Testing simple input..."
echo "VoidBox{test}" | ./KeyForge

echo ""
echo "Extracting strings..."
strings KeyForge | grep -iE "(enter|license|key|valid|format|void|correct|wrong|success)"

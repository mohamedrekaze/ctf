#!/usr/bin/env python3
"""
Final angr attempt with better configuration
"""
import angr
import claripy

binary_path = './KeyForge'

# Load the binary
print("Loading binary...")
p = angr.Project(binary_path, auto_load_libs=False)

# Create initial state at main
print("Creating initial state...")
state = p.factory.entry_state()

# Create symbolic input - exactly 36 bytes
flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(36)]
flag = claripy.Concat(*flag_chars)

# Add constraints for known format
# DeepSec{...}\n
for i, c in enumerate(b'DeepSec{'):
    state.solver.add(flag_chars[i] == c)

state.solver.add(flag_chars[35] == ord('}'))

# Add constraints for known part: wh0_s41d_y0
known = b'wh0_s41d_y0'
for i, c in enumerate(known):
    state.solver.add(flag_chars[8 + i] == c)

# Constrain remaining to printable ASCII  
for i in range(19, 35):
    state.solver.add(flag_chars[i] >= ord('0'))
    state.solver.add(flag_chars[i] <= ord('z'))

# Add stdin
state.posix.stdin.store(0, flag)
state.posix.stdin.store(36, claripy.BVV(b'\n'))

# Create simulation manager
print("Creating simulation manager...")
simgr = p.factory.simulation_manager(state)

# Find "License valid!" and avoid "failed" and "Invalid"
print("Starting symbolic execution (this may take a while)...")
print("Exploring up to 500 steps...")

simgr.explore(
    find=lambda s: b"License valid!" in s.posix.dumps(1),
    avoid=lambda s: b"Invalid format" in s.posix.dumps(1) or b"validation failed" in s.posix.dumps(1),
    step_func=lambda sm: print(f"Active: {len(sm.active)}, Found: {len(sm.found)}, Avoided: {len(sm.avoid)}, Steps: {sm._hierarchy.num_steps}") or sm,
    num_find=1
)

print(f"\nExploration complete!")
print(f"Found: {len(simgr.found)} states")
print(f"Active: {len(simgr.active)} states") 
print(f"Avoided: {len(simgr.avoid)} states")

if simgr.found:
    print("\n" + "="*60)
    print("SOLUTION FOUND!")
    print("="*60)
    found_state = simgr.found[0]
    solution = found_state.posix.dumps(0)
    print(f"Flag: {solution[:36].decode(errors='ignore')}")
else:
    print("\nNo solution found. Try increasing exploration depth or adjusting constraints.")


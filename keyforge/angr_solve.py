#!/usr/bin/env python3
"""
Solve KeyForge using angr symbolic execution
"""
import angr
import claripy
import sys

print("Loading binary...")
project = angr.Project('./KeyForge', auto_load_libs=False)

print("Creating symbolic input...")
# Create symbolic input for the license key (36 bytes + newline)
flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(36)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

# Set up initial state
initial_state = project.factory.full_init_state(
    args=['./KeyForge'],
    add_options=angr.options.unicorn,
    stdin=flag
)

# Add constraints for known format: DeepSec{...}
known_prefix = b"DeepSec{"
for i, char in enumerate(known_prefix):
    initial_state.solver.add(flag_chars[i] == char)

# Last character must be '}'
initial_state.solver.add(flag_chars[35] == ord('}'))

# Add constraints: characters must be printable
for i in range(8, 35):  # Inside the braces
    initial_state.solver.add(flag_chars[i] >= 0x20)  # Printable ASCII
    initial_state.solver.add(flag_chars[i] <= 0x7e)

print("Starting symbolic execution...")
print("Looking for 'License valid!' message...\n")

# Define success and failure conditions
def is_successful(state):
    output = state.posix.dumps(1)  # stdout
    return b"License valid!" in output

def is_failed(state):
    output = state.posix.dumps(1)
    return b"Invalid format" in output or b"License validation failed" in output

# Create simulation manager with exploration technique
simgr = project.factory.simulation_manager(initial_state)

# Use explorer technique
simgr.use_technique(angr.exploration_techniques.Explorer(find=is_successful, avoid=is_failed))

# Explore until we find a solution
try:
    step_count = 0
    while simgr.active and not simgr.found:
        simgr.step()
        step_count += 1
        if step_count % 10 == 0:
            print(f"Steps: {step_count}, Active: {len(simgr.active)}, Found: {len(simgr.found)}, Deadended: {len(simgr.deadended)}", end='\r')
        
        # Stop if taking too long or too many paths
        if step_count > 1000 or len(simgr.active) > 50:
            print(f"\nStopping: too complex (steps={step_count}, active={len(simgr.active)})")
            break
    
    print("\n")
    
    if simgr.found:
        print("=" * 60)
        print("SOLUTION FOUND!")
        print("=" * 60)
        
        solution_state = simgr.found[0]
        solution = solution_state.posix.dumps(0)[:36]  # Get the input
        
        print(f"Flag: {solution.decode('utf-8', errors='replace')}")
        print()
        
        # Verify with actual binary
        import subprocess
        result = subprocess.run(['./KeyForge'], input=solution + b'\n',
                              capture_output=True, timeout=2)
        print("Verification:")
        print(result.stdout.decode())
    else:
        print("No solution found.")
        print(f"Explored {step_count} steps")
        
except KeyboardInterrupt:
    print("\n\nInterrupted by user")
    sys.exit(1)
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

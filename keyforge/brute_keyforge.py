#!/usr/bin/env python3
"""
Solve KeyForge by brute-forcing character by character
"""
import subprocess
import string

def test_flag(flag):
    """Test a flag and return True if it passes validation"""
    result = subprocess.run(['./KeyForge'], input=flag + '\n',
                          capture_output=True, text=True, timeout=1)
    output = result.stdout.strip()
    
    if "License valid!" in output:
        return "VALID"
    elif "License validation failed" in output:
        return "FAILED"
    elif "Invalid format" in output:
        return "FORMAT"
    else:
        return "UNKNOWN"

# We know the format: DeepSec{XXXXXXXXXXXXXXXXXXXXXXXXXXX}
#                      012345678901234567890123456789012345
#                                1111111111222222222233333

# Start with all A's
known = "DeepSec{" + "A" * 27 + "}"

# Character set to try
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_ !@#$%^&*()-+=[]{}|;:',.<>?/"

print(f"Initial: {known}")
print(f"Status: {test_flag(known)}")
print()

# Try brute forcing position by position
# But this is too slow. Let me try the hint string directly
hints = [
    "slak ajmi regle le osf le li",  # 28 chars - too long
    "slak ajmi regle le osf le ",     # 26 chars
    "slak_ajmi_regle_le_osf_le_",     # 27 chars - with underscores
]

for hint in hints:
    if len(hint) == 27:
        flag = "DeepSec{" + hint + "}"
        status = test_flag(flag)
        print(f"{flag}: {status}")

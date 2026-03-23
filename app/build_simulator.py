import os

BUILD_FILE = "dataset/current_build.txt"

def generate_build(mode="clean"):

    if mode == "clean":
        content = """
login_function
api_request
data_processing
normal_operation
"""

    elif mode == "medium":
        content = """
api_call
unknown_network
base64_encoded_payload
suspicious_request
"""

    elif mode == "critical":
        content = """
cmd.exe
powershell
reverse_shell
data_exfiltration
malware_payload
"""

    else:
        content = "unknown build"

    with open(BUILD_FILE, "w") as f:
        f.write(content)

    print(f"✔ Build generated in {mode.upper()} mode")

    return BUILD_FILE


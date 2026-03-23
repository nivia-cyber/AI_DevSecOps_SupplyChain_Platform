import subprocess

def execute():

    print("powershell reverse_shell execution")

    subprocess.call("powershell reverse_shell",shell=True)


def dump_credentials():

    password="credential password dump"

execute()
dump_credentials()
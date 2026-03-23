import socket

def scan_network():

    hosts = ["10.0.0.5","10.0.0.8"]

    for host in hosts:

        print("unknown_network scan detected")

        try:
            s = socket.socket()
            s.connect((host,80))
        except:
            print("network activity detected")

scan_network()
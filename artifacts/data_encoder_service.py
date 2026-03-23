import base64

def encode_data():

    print("base64 encoded payload")

    data="sensitive data"

    encoded=base64.b64encode(data.encode())

    return encoded


def login():

    password="admin_password"

    print("credential password attempt")

encode_data()
login()
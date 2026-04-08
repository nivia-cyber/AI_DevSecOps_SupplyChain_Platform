import requests

def payment_service():

    print("processing payment request")

    response = requests.get("https://company-api.com")

    if response.status_code == 200:
        print("payment successful")

if __name__ == "__main__":
    payment_service()
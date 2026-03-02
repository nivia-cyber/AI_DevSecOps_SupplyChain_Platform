import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def push_to_github(local_file_path, repo_file_path):

    with open(local_file_path, "rb") as f:
        content = f.read()

    encoded_content = base64.b64encode(content).decode()

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{repo_file_path}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if file exists to get SHA
    get_response = requests.get(url, headers=headers)

    data = {
        "message": "Auto deployment from AI DevSecOps Security Platform",
        "content": encoded_content,
        "branch": "main"
    }

    if get_response.status_code == 200:
        file_data = get_response.json()
        data["sha"] = file_data["sha"]

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print("Code successfully pushed to GitHub.")
    else:
        print("GitHub push failed:", response.json())
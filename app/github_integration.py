import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def push_to_github(file_path, repo_file_path):

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{repo_file_path}"

    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    data = {
        "message": "Auto deployment from AI DevSecOps Security Platform",
        "content": content
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print("Code successfully pushed to GitHub.")
    else:
        print("GitHub push failed:", response.json())
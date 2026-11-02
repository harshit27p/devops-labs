import os
import requests
from requests.auth import HTTPBasicAuth

def create_ticket(summary: str, description: str) -> dict:
    base_url = os.environ["TICKETING_BASE_URL"].rstrip("/")
    payload = {
        "fields": {
            "project": {"key": os.environ["TICKETING_PROJECT_KEY"]},
            "summary": summary,
            "issuetype": {"name": "Task"},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}]
                }]
            }
        }
    }
    response = requests.post(
        f"{base_url}/rest/api/3/issue",
        json=payload,
        auth=HTTPBasicAuth(
            os.environ["TICKETING_EMAIL"],
            os.environ["TICKETING_API_TOKEN"],
        ),
        headers={"Accept": "application/json"},
        timeout=(3, 15),
    )
    response.raise_for_status()
    return response.json()

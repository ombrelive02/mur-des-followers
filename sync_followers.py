import os
import json
import urllib.parse
import urllib.request

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_CLIENT_SECRET"]
broadcaster_id = os.environ["TWITCH_BROADCASTER_ID"]

def request_json(url, headers=None, data=None):
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

token_data = request_json(
    "https://id.twitch.tv/oauth2/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data=urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }).encode()
)

headers = {
    "Client-ID": client_id,
    "Authorization": "Bearer " + token_data["access_token"]
}

followers = []
cursor = None

while True:
    params = {"broadcaster_id": broadcaster_id, "first": 100}
    if cursor:
        params["after"] = cursor

    url = "https://api.twitch.tv/helix/channels/followers?" + urllib.parse.urlencode(params)
    result = request_json(url, headers=headers)

    followers.extend(item["user_name"] for item in result["data"])
    cursor = result.get("pagination", {}).get("cursor")
    if not cursor:
        break

with open("followers.json", "w", encoding="utf-8") as file:
    json.dump(followers, file, ensure_ascii=False, indent=2)

print(f"{len(followers)} followers enregistrés")

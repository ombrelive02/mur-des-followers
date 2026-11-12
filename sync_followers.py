
import os
import json
import urllib.parse
import urllib.request

client_id = os.environ["TWITCH_CLIENT_ID"]
broadcaster_id = os.environ["TWITCH_BROADCASTER_ID"]
access_token = os.environ["TWITCH_USER_ACCESS_TOKEN"]

followers = []
cursor = None

while True:
    params = {
        "broadcaster_id": broadcaster_id,
        "first": 100
    }

    if cursor:
        params["after"] = cursor

    url = (
        "https://api.twitch.tv/helix/channels/followers?"
        + urllib.parse.urlencode(params)
    )

    request = urllib.request.Request(
        url,
        headers={
            "Client-ID": client_id,
            "Authorization": "Bearer " + access_token
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)

    followers.extend(
        item["user_name"] for item in result["data"]
    )

    cursor = result.get("pagination", {}).get("cursor")

    if not cursor:
        break

with open("followers.json", "w", encoding="utf-8") as file:
    json.dump(followers, file, ensure_ascii=False, indent=2)

print(f"{len(followers)} followers enregistrés")

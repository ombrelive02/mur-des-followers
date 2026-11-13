
import os
import json
import urllib.parse
import urllib.request

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_CLIENT_SECRET"]
broadcaster_id = os.environ["TWITCH_BROADCASTER_ID"]
refresh_token = os.environ["TWITCH_REFRESH_TOKEN"]

def requete(url, donnees=None, headers=None):
    req = urllib.request.Request(
        url,
        data=donnees,
        headers=headers or {}
    )
    with urllib.request.urlopen(req, timeout=30) as rep:
        return json.load(rep)

# Renouveler le jeton Twitch
donnees = urllib.parse.urlencode({
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
}).encode()

tokens = requete(
    "https://id.twitch.tv/oauth2/token",
    donnees,
    {"Content-Type": "application/x-www-form-urlencoded"}
)

access_token = tokens["access_token"]

headers = {
    "Client-ID": client_id,
    "Authorization": "Bearer " + access_token
}

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

    resultat = requete(url, headers=headers)

    followers.extend(
        utilisateur["user_name"]
        for utilisateur in resultat["data"]
    )

    cursor = resultat.get("pagination", {}).get("cursor")

    if not cursor:
        break

with open("followers.json", "w", encoding="utf-8") as fichier:
    json.dump(followers, fichier, ensure_ascii=False, indent=2)

print(f"{len(followers)} followers enregistrés")


import os
import json
import base64
import hashlib
import urllib.parse
import urllib.request
from cryptography.fernet import Fernet

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_CLIENT_SECRET"]
broadcaster_id = os.environ["TWITCH_BROADCASTER_ID"]
cle = os.environ["TWITCH_TOKEN_KEY"]

cle_derivee = base64.urlsafe_b64encode(
    hashlib.sha256(cle.encode("utf-8")).digest()
)
chiffrement = Fernet(cle_derivee)

with open("twitch_tokens.enc", "rb") as fichier:
    tokens = json.loads(chiffrement.decrypt(fichier.read()))

donnees = urllib.parse.urlencode({
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "refresh_token",
    "refresh_token": tokens["refresh_token"]
}).encode("utf-8")

requete = urllib.request.Request(
    "https://id.twitch.tv/oauth2/token",
    data=donnees,
    method="POST"
)

with urllib.request.urlopen(requete, timeout=30) as reponse:
    nouveaux_tokens = json.load(reponse)

with open("twitch_tokens.enc", "wb") as fichier:
    fichier.write(chiffrement.encrypt(json.dumps({
        "access_token": nouveaux_tokens["access_token"],
        "refresh_token": nouveaux_tokens["refresh_token"]
    }).encode("utf-8")))

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

    requete = urllib.request.Request(
        url,
        headers={
            "Client-ID": client_id,
            "Authorization": "Bearer " + nouveaux_tokens["access_token"]
        }
    )

    with urllib.request.urlopen(requete, timeout=30) as reponse:
        resultat = json.load(reponse)

    followers.extend(
        utilisateur["user_name"]
        for utilisateur in resultat["data"]
    )

    cursor = resultat.get("pagination", {}).get("cursor")
    if not cursor:
        break

with open("followers.json", "w", encoding="utf-8") as fichier:
    json.dump(followers, fichier, ensure_ascii=False, indent=2)

print(f"{len(followers)} followers enregistres")

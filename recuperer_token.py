
import os
import json
import urllib.parse
import urllib.request
import base64
import hashlib

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_CLIENT_SECRET"]
code = os.environ["TWITCH_AUTH_CODE"]
cle = os.environ["TWITCH_TOKEN_KEY"]

donnees = urllib.parse.urlencode({
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": "https://ombrelive02.github.io/mur-des-followers/"
}).encode("utf-8")

requete = urllib.request.Request(
    "https://id.twitch.tv/oauth2/token",
    data=donnees,
    method="POST"
)

with urllib.request.urlopen(requete, timeout=30) as reponse:
    tokens = json.load(reponse)

from cryptography.fernet import Fernet

cle_derivee = base64.urlsafe_b64encode(
    hashlib.sha256(cle.encode("utf-8")).digest()
)

chiffrement = Fernet(cle_derivee)

contenu = json.dumps({
    "access_token": tokens["access_token"],
    "refresh_token": tokens["refresh_token"]
}).encode("utf-8")

with open("twitch_tokens.enc", "wb") as fichier:
    fichier.write(chiffrement.encrypt(contenu))

print("Jetons Twitch recuperes et chiffres avec succes.")

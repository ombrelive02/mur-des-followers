
import os
import urllib.parse
import urllib.request
import json

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_CLIENT_SECRET"]
code = os.environ["TWITCH_AUTH_CODE"]

data = urllib.parse.urlencode({
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": "https://ombrelive02.github.io/mur-des-followers/"
}).encode("utf-8")

request = urllib.request.Request(
    "https://id.twitch.tv/oauth2/token",
    data=data,
    method="POST"
)

with urllib.request.urlopen(request, timeout=30) as response:
    tokens = json.load(response)

print("Autorisation Twitch réussie.")
print("Ne publie jamais les jetons d'accès ou de renouvellement.")

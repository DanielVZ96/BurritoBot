import requests
import json

CLIENT_ID = 'SECRET'
CLIENT_SECRET_ID = 'SECRET'
REDIRECT_URI = 'https://www.devz.cl/burritobot/login/'
# REDIRECT_URI = 'http://127.0.0.1:8000/burritobot_app/login/'


def authorize_request(scope):
    request = 'https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={}&redirect_uri={}&scope={}'.format(CLIENT_ID,REDIRECT_URI,scope)
    return request


def token_request(code):
    url = 'https://api.twitch.tv/kraken/oauth2/token?client_id={}&client_secret={}&code={}&grant_type=authorization_code&redirect_uri={}'.format(CLIENT_ID, CLIENT_SECRET_ID, code, REDIRECT_URI)
    request = requests.post(url)
    response_dict = json.loads(request.text)
    print(response_dict)
    return response_dict


def get_user_dict(token):
    url = 'https://api.twitch.tv/kraken/user'
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': CLIENT_ID,
        'Authorization': 'OAuth {}'.format(token)
    }
    request = requests.get(url, headers=headers)
    return json.loads(request.text)

def refresh_token(token):
    url = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=refresh_token&refresh_token={}'.format(CLIENT_ID, CLIENT_SECRET_ID, token)
    response = requests.post(url)
    if response.status_code == requests.codes.ok:
        return response.json()

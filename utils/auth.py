import requests
global CLIENT_ID
import json
global CLIENT_SECRET_ID
CLIENT_ID = 'vkanazzpgcy7w9rfhvbgp2pmdw74g6'
CLIENT_SECRET_ID = '92um4d83q6rgl1f92oamuokqatbua2'
REDIRECT_URI = 'http://localhost:8000/burritobot/login/'

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
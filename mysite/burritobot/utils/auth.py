from urllib.request import urlopen
from json import dump

CLIENT_ID = 'vkanazzpgcy7w9rfhvbgp2pmdw74g6'
CLIENT_SECRET_ID = '92um4d83q6rgl1f92oamuokqatbua2'

def new_user_token_request(redirect_uri, scope):
    request = 'https://id.twitch.tv/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}'.format(CLIENT_ID,redirect_uri,scope)
    return request

def new_access_token_request(redirect_uri, code):
    request = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&code={}&grant_type=authorization_code&redirect_uri={}'.format(CLIENT_ID, CLIENT_SECRET_ID, code, redirect_uri)
    response = urlopen(request)
    response_dict = dump(response)
    return response_dict
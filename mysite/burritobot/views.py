from django.shortcuts import render
from ..utils import auth
from .models import AuthInfo
import datetime

def register(request):
    get_request = auth.new_user_token_request('https://www.devz.cl/authenticated/','chat_login+channel_subscriptions+channel_editor+channel_check_subscription')
    context = {'get_request':get_request}
    return render(request, 'burritobot/register.html', context)

def authenticated(request, code):
    token_dict = auth.new_access_token_request('https://www.devz.cl/authenticated/', code)
    new_auth = AuthInfo()
    new_auth.expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(token_dict['expires_in']))
    new_auth.access_token = token_dict['access_token']
    new_auth.refresh_token = token_dict['refresh_token']
    new_auth.scope = token_dict['scope']
    new_auth.save()
    return render(request, 'burritobot/commands.html', {})

def commands(request):
    render(request, 'burritobot/commands.html', {})
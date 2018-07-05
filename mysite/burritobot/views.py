from django.shortcuts import render
from .models import AuthInfo, Command
from django.forms import formset_factory
from .utils import auth
from .forms import CommandForm, CommandFormSet
import datetime

def register(request):
    if 'code' in request.GET:
        print('SUCCESS!')
        code = request.GET['code']
        print('code: ' + code)
        scope = request.GET['scope']
        print('scope: ' + scope)
        auth_dict = auth.token_request(code)
        expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(auth_dict['expires_in']))
        new_auth = AuthInfo(access_token=auth_dict['access_token'], refresh_token=auth_dict['refresh_token'], expiration_date=expiration_date, scope=scope)
        new_auth.save()
        return commands(request)
    else:
        get_request = auth.authorize_request('chat_login')
        context = {'get_request':get_request}
        return render(request, 'burritobot/register.html', context)




def authenticated(request, code):
    token_dict = auth.new_access_token_request('http://127.0.0.1:8000/authenticated', code)
    new_auth = AuthInfo()
    new_auth.expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(token_dict['expires_in']))
    new_auth.access_token = token_dict['access_token']
    new_auth.refresh_token = token_dict['refresh_token']
    new_auth.scope = token_dict['scope']
    new_auth.save()
    return render(request, 'burritobot/commands.html', {})


def edit_commands(request):
    new_command_form = CommandForm(prefix='new-command')
    if request.method == 'GET':
        command_formset = CommandFormSet(prefix='existing-commands')
        return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})
    if request.method == 'POST':
        command_formset = CommandFormSet(request.POST, request.FILES, prefix='existing-commands')
        if command_formset.is_valid():
            command_formset.save()
        return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})


def new_commands(request):
    command_formset = CommandFormSet(prefix='existing-commands')
    new_command_form = CommandForm(prefix='new-command')
    if request.method == 'GET':
        return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})
    if request.method == 'POST':
        new_command_form = CommandForm(request.POST, prefix='new-command')
        if new_command_form.is_valid():
            new_command_form.save()
        return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})


def commands(request):
    command_formset = CommandFormSet(prefix='existing-commands')
    new_command_form = CommandForm(prefix='new-command')
    return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})

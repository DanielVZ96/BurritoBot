from django.shortcuts import render
from .models import AuthInfo, Command, CommandForm
from django.forms import formset_factory
from .utils import auth
import datetime

def register(request):
    if request.method == 'GET':
        try:
            code = request.POST['code']
            scope = request.POST['scope']
            auth.new_access_token_request('http://127.0.0.1:8000/burrito/authenticated', code)
            return render(request, 'commands.html', {})
        except:
            get_request = auth.new_user_token_request('http://127.0.0.1:8000/burrito/authenticated','chat_login+channel_subscriptions+channel_editor+channel_check_subscription')
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
    CommandFormSet = formset_factory(CommandForm)
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
    CommandFormSet = formset_factory(CommandForm)
    command_formset = CommandFormSet(prefix='existing-commands')
    new_command_form = CommandForm(prefix='new-command')
    if request.method == 'GET':
        return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})
    if request.method == 'POST':
        new_command_form = CommandForm(request.POST, prefix='new-command')
        if new_command_form.is_valid():
            new_command_form.save()
        return render(request, 'burritobot/commands.html', {'command_formset':command_formset, 'new_command_form':new_command_form})

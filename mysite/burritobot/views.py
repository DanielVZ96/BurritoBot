from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import TwitchUser, Command
from .utils import auth
from .forms import CommandForm, CommandFormSet
import datetime

def login_view(request):
    if request.user.is_authenticated:
        print('AUTHENTICATED')
        return commands(request)

    if 'code' in request.GET:
        # Get info from request necessary to make token request
        code = request.GET['code']
        scope = request.GET['scope']

        # Call auth function to get new auth info
        auth_dict = auth.token_request(code)
        expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(auth_dict['expires_in']))

        # Call auth function to get user info with the token provided by twitch
        user_dict = auth.get_user_dict(auth_dict['access_token'])

        try:
            # If the user exists, update it's auth info.
            twitch_user = TwitchUser.objects.get(twitch_id=int(user_dict['_id']))
            user = User.objects.get(username=twitch_user.twitch_id)
            twitch_user.access_token, twitch_user.refresh_token, twitch_user.expiration_date, twitch_user.scope = auth_dict['access_token'], auth_dict['refresh_token'], expiration_date, auth_dict['scope']
            user.set_password(twitch_user.access_token)
            user.save()
            twitch_user.save()

            # Authenticate
            user = authenticate(username=twitch_user.twitch_id, password=twitch_user.access_token)
            print('User {} UPDATED! New token: {}'.format(twitch_user.twitch_name, twitch_user.access_token))
        except TwitchUser.DoesNotExist:

            # If user doesn't exist, create new one with parameters given by auth and user info.
            user = User.objects.create_user(username=user_dict['_id'], email=user_dict['email'], password=auth_dict['access_token'])
            twitch_user = TwitchUser(twitch_id=int(user_dict['_id']), twitch_name=user_dict['display_name'], email=user_dict['email'], access_token=auth_dict['access_token'], refresh_token=auth_dict['refresh_token'], expiration_date=expiration_date, scope=scope, user=user)
            twitch_user.save()
            user = authenticate(username=user_dict['display_name'], password=None)
            print('User {} CREATED'.format(twitch_user.twitch_name))
            login(request, user)
            return commands(request)

        # Log in User and render commands
        if user is not None:
            login(request, user)
            print('User LOGED IN')
        return commands(request)

    else:
        # If this request doesn't have 'code', we request it and render the view again to further process 'code'
        get_request = auth.authorize_request('chat_login+user_read+channel_feed_edit')
        context = {'get_request':get_request}

    return render(request, 'burritobot/login.html', context)


# TODO MAKE COMMAND VIEWS USE THE AUTH BACKEND
@login_required(login_url='/burritobot/login/')
def edit_commands(request):
    if request.method == 'POST':
        command_formset = CommandFormSet(request.POST, request.FILES, prefix='existing-commands')
        if command_formset.is_valid():
            command_instances = command_formset.save(commit=False)
            for obj in command_formset.deleted_objects:
                obj.delete()
            for edited_command in command_instances:
                edited_command.user = request.user
                edited_command.save()
    return commands(request)


@login_required(login_url='/burritobot/login/')
def new_commands(request):
    if request.method == 'POST':
        new_command_form = CommandForm(request.POST, prefix='new-command')
        if new_command_form.is_valid():
            new_command = new_command_form.save(commit=False)
            new_command.user = request.user
            new_command.save()
    return commands(request)


@login_required(login_url="/burritobot/login/")
def commands(request):
    command_formset = CommandFormSet(prefix='existing-commands')
    new_command_form = CommandForm(prefix='new-command')
    return render(request, 'burritobot/commands.html', {'command_formset': command_formset, 'new_command_form': new_command_form})

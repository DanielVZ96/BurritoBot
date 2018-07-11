import requests
import json


def _get_ids(game, category, variable=False, value=False):
    game_url = 'https://www.speedrun.com/api/v1/games/{}'.format(game)
    game_req = requests.get(game_url)
    game_data = json.loads(game_req.text)['data']
    game_id = game_data['id']

    categories_uri, variables_uri = [x['uri'] for x in list(filter(lambda d: d['rel'] == 'variables' or d['rel'] == 'categories', game_data['links']))]

    categories_req = requests.get(str(categories_uri))
    categories_data = json.loads(categories_req.text)['data']
    category_data = list(filter(lambda d: category == d['name'], categories_data))[0]
    category_id = category_data['id']

    if variable:
        variables_req = requests.get(str(variables_uri))
        variables_data = json.loads(variables_req.text)['data']
        variable_data = list(filter(lambda d: variable == d['name'], variables_data))[0]
        variable_id = variable_data['id']
        if value:
            values_data = variable_data['values']['values']
            value_id = [k for k,v in values_data.items() if v['label'] == value][0]
            return game_id,category_id, variable_id,value_id
        return game_id,category_id, variable_id
    return game_id,category_id


def get_top_str(game, category, variable=False, value=False):
    url = 'https://www.speedrun.com/api/v1/leaderboards'
    if value and variable:
        game_id, category_id, variable_id, value_id = _get_ids(game, category, variable, value)
        leaderboard_url = '{}/{}/category/{}?var-{}={}'.format(url, game_id, category_id, variable_id, value_id)
    else:
        game_id, category_id = _get_ids(game, category)
        leaderboard_url = '{}/{}/category/{}'.format(url, game_id, category_id)

    req = requests.get(leaderboard_url)
    runs_data = json.loads(req.text)['data']['runs']
    runs = [run for run in runs_data if int(run['place'])<=5]

    ret = ''
    for run in runs:
        run_place = int(run['place'])
        run_time = run['run']['times']['primary'][2:].lower()

        run_user_uri = run['run']['players'][0]['uri']
        req = requests.get(run_user_uri)
        user_name = json.loads(req.text)['data']['names']['international']
        ret += '{}) {}: {}  '.format(run_place, user_name, run_time)
    return ret


def existing_commands():
    return ['top']


def super_command(command):
    command_root = command.split(" ")[0]
    if len(command[4:].split('/')) < 2:
        return 'Please add enough parameters'
    if command_root.strip() == 'top':
        print('top called!')
        params = command[4:].split('/')
        try:
            if len(params) == 4:
                g, c, v, va = params
                return get_top_str(g,c,v,va)
            else:
                g, c = params[:2]
                return get_top_str(g,c)
        except KeyError:
            return "Couldn't find any run like that. Try another formating (¿top)."


if __name__=='__main__':
    print(_get_ids('botw', 'Any%', 'Amiibo', 'No Amiibo'))
    print(get_top_str('botw', 'Any%', 'Amiibo'))

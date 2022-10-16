from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from discord_oauth2 import DiscordAuth
from configparser import ConfigParser
import os, requests, json


@view_config(route_name='colors', renderer='cl_discord_self_service:templates/colors.jinja2')
def my_view(request):
    configure = ConfigParser()
    configure.read('config.ini')

    client_id = configure.get('discord', 'client-id')
    client_secret = configure.get('discord', 'client_secret')
    callback_url = configure.get('discord', 'callback-url')
    app_token = callback_url = configure.get('discord', 'app-token')

    discord_auth = DiscordAuth(client_id, client_secret, callback_url)

    session = request.session
    user_data = discord_auth.get_user_data_from_token(session['magick']['access_token'])
    user_id = user_data['id']
    new_color = request.params['color']

    colors = {"strawberry": "722481631591399484", 
            "magma": "722480272204890113",
            "saturn": "921573908845588480",
            "lemon": "722463939933503551",
            "kiwi": "722460654019280998",
            "green_apple": "722464058590363669",
            "sauropod": "722474287801303040",
            "ocean": "722476867919020102",
            "blueberry": "722476184012587088",
            "yinmn": "956594507263148032",
            "grape": "722467658792042567",
            "magenta": "722464493187104768",
            "pink": "722506272968147034"}

    user_profile_header = {"Authorization": "Bot " + app_token}
    user_profile_req = requests.get('https://discord.com/api/guilds/71992212115697664/members/' + user_id, headers=user_profile_header)
    user_profile = json.loads(user_profile_req.text)

    curr_roles = user_profile['roles']

    for x in colors.values():
        for y in curr_roles:
            if y == x:
                requests.delete('https://discord.com/api/guilds/71992212115697664/members/' + user_id + '/roles/' + x, headers=user_profile_header)
                break
    
    requests.put('https://discord.com/api/guilds/71992212115697664/members/' + user_id + '/roles/' + colors[new_color], headers=user_profile_header)

    return {'project': 'CL Discord Self-Service', 'user': user_data['username'], 'discrim': user_data['discriminator'], "color": new_color}


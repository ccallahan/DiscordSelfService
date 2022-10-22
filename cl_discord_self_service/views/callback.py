from lib2to3.pgen2 import token
from urllib import response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from discord_oauth2 import DiscordAuth
from configparser import ConfigParser
import os

@view_config(route_name='callback')
def callback_view(request):
    configure = ConfigParser()
    configure.read('/opt/DiscordSelfService/cl_discord_self_service/config.ini')

    client_id = configure.get('discord', 'client-id')
    client_secret = configure.get('discord', 'client_secret')
    callback_url = configure.get('discord', 'callback-url')

    discord_auth = DiscordAuth(client_id, client_secret, callback_url)
    session = request.session
    auth_code = request.params['code']

    tokens = discord_auth.get_tokens(auth_code)
    session['magick'] = tokens
    return HTTPFound(location="/")





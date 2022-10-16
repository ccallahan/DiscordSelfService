from lib2to3.pgen2 import token
from urllib import response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from discord_oauth2 import DiscordAuth
import os

@view_config(route_name='callback')
def callback_view(request):
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    callback_url = os.environ['CALLBACK_URL']

    discord_auth = DiscordAuth(client_id, client_secret, callback_url)
    session = request.session
    auth_code = request.params['code']

    tokens = discord_auth.get_tokens(auth_code)
    session['magick'] == tokens
    return HTTPFound(location="/")





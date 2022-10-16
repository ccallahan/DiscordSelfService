from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from discord_oauth2 import DiscordAuth
from configparser import ConfigParser

@view_config(route_name='home', renderer='cl_discord_self_service:templates/home.jinja2')
def my_view(request):
    configure = ConfigParser()
    configure.read('config.ini')

    client_id = configure.get('discord', 'client-id')
    client_secret = configure.get('discord', 'client_secret')
    callback_url = configure.get('discord', 'callback-url')
    stripe_api = configure.get('stripe','public-key')

    discord_auth = DiscordAuth(client_id, client_secret, callback_url)
    session = request.session


    if 'magick' in session:
        user_data = discord_auth.get_user_data_from_token(session['magick']['access_token'])
        return {'project': 'CL Discord Self-Service', 'user': user_data['username'], 'discrim': user_data['discriminator'], 'stripe_api': stripe_api}
    else:
        login_url = discord_auth.login()
        return HTTPFound(location=login_url)
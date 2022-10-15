from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from discord_oauth2 import DiscordAuth
import os

@view_config(route_name='home', renderer='cl_discord_self_service:templates/home.jinja2')
def my_view(request):
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    callback_url = os.environ['CALLBACK_URL']
    stripe_api = os.environ['STRIPE_API']

    discord_auth = DiscordAuth(client_id, client_secret, callback_url)
    session = request.session


    if 'magick' in session:
        user_data = discord_auth.get_user_data_from_token(session['magick']['access_token'])
        return {'project': 'CL Discord Self-Service', 'user': user_data['username'], 'discrim': user_data['discriminator'], 'stripe_api': stripe_api}
    else:
        login_url = discord_auth.login()
        return HTTPFound(location=login_url)
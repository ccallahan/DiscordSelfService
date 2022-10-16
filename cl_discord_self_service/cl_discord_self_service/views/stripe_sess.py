from pyramid.response import Response
from pyramid.view import view_config
from discord_oauth2 import DiscordAuth
from configparser import ConfigParser
import stripe


@view_config(route_name='stripe_sess')
def my_view(request):
    configure = ConfigParser()
    configure.read('config.ini')

    client_id = configure.get('discord', 'client-id')
    client_secret = configure.get('discord', 'client_secret')
    callback_url = configure.get('discord', 'callback-url')
    stripe.api_key = configure.get('stripe','secret-key')




    discord_auth = DiscordAuth(client_id, client_secret, callback_url)
    session = request.session

    user_data = discord_auth.get_user_data_from_token(session['magick']['access_token'])
    # In the route handler for /create-verification-session:
    # Authenticate your user.

    # Create the session.

    verification_session = stripe.identity.VerificationSession.create(
    type='document',
    metadata={
        'user_id': user_data['id'],
    },
    )

    stripe_response = '{"client_secret": "' + verification_session.client_secret + '"}'

    return Response(stripe_response, content_type='text/json')
from pyramid.response import Response
from pyramid.view import view_config
from discord_oauth2 import DiscordAuth
import stripe
import os


@view_config(route_name='stripe_sess')
def my_view(request):
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    callback_url = os.environ['CALLBACK_URL']
    api_key = os.environ['STRIPE_SECRET']
    stripe.api_key = api_key


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
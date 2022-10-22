from pyramid.response import Response
from pyramid.view import view_config
import stripe, requests, os


@view_config(route_name='nsfw_grant')
def my_view(request):
    stripe.api_key = os.environ['STRIPE_SECRET']
    endpoint_secret = os.environ['STRIPE_WHSEC']

    app_token = configure.get('discord', 'app-token')
    user_profile_header = {"Authorization": "Bot " + app_token}

    signature = request.headers.get('stripe-signature')
    payload = request.body

    # Verify webhook signature and extract the event.
    # See https://stripe.com/docs/webhooks/signatures for more information.
    try:
        event = stripe.Webhook.construct_event(
        payload=payload,
        sig_header=signature,
        secret=endpoint_secret,
        )
    except ValueError as e:
        # Invalid payload.
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid Signature.
        return Response(status=400)

    if event['type'] == 'identity.verification_session.verified':
        verification_session = event.data.object
        user_id = verification_session['metadata']['user_id']
        requests.put('https://discord.com/api/guilds/71992212115697664/members/' + user_id + '/roles/393666167895752715', headers=user_profile_header)
        requests.put('https://discord.com/api/guilds/71992212115697664/members/' + user_id + '/roles/313491151535472640', headers=user_profile_header)


    return Response(status=200)
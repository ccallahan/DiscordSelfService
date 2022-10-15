from pyramid.response import Response
from pyramid.view import view_config
import stripe
import os
import requests


@view_config(route_name='nsfw_grant')
def my_view(request):
    stripe.api_key = 'sk_test_51LtIR9A8Urc1SRYguyPEvVd5cmkXAXPoW8hrFbX6vCl54vhlLySvLiAuDwZu4IY0xWSiZVoD4sUaYq33LIi22EIX00gvyVylT7'
    endpoint_secret = 'whsec_82131648de2a807cc5ba6c9cacbc0ffe8e26cc18733c529c39a94c727d4e6643'

    app_token = os.environ['APP_TOKEN']
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
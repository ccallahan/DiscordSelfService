from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
import os

def main(global_config, **settings):
    env_secret = os.environ['MAGICK']
    my_session_factory = SignedCookieSessionFactory(env_secret)

    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.set_session_factory(my_session_factory)
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()

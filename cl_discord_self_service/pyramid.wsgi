from pyramid.paster import get_app, setup_logging
ini_path = '/opt/DiscordSelfService/cl_discord_self_service/production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
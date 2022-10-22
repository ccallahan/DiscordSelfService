def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('callback', '/callback')
    config.add_route("colors", "/colors")
    config.add_route("stripe_sess", "/stripe-sess")
    config.add_route("nsfw_grant", "/nsfw-grant")
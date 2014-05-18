import logging
import secrets

import webapp2
import gae_mini_profiler.profiler
import gae_mini_profiler.templatetags

logger = logging.getLogger(__name__)


config = {}
config['webapp2_extras.sessions'] = {
            'secret_key': secrets.SESSION_KEY,
}
config['webapp2_extras.jinja2'] = {
        'globals': {
            'uri_for': webapp2.uri_for,
            'profiler_includes': gae_mini_profiler.templatetags.profiler_includes,
        }
}



app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler='tracker.handlers.Index', name='index'),
    webapp2.Route(r'/home',
        handler='tracker.handlers.Home',
        name='home'),
    webapp2.Route(r'/confirm/', handler='tracker.handlers.Confirmation',
        name='confirm'),
    webapp2.Route(r'/auth/<provider>',
        handler='authentication.handlers.AuthHandler:_simple_auth',
        name='auth_login'),
    webapp2.Route(r'/auth/<provider>/callback',
        handler='authentication.handlers.AuthHandler:_auth_callback',
        name='auth_callback'),
    webapp2.Route(r'/logout',
        handler='authentication.handlers.AuthHandler:logout', name='logout'),
    ], config=config, debug=True)

app = gae_mini_profiler.profiler.ProfilerWSGIMiddleware(app)

def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app


def gae_mini_profiler_should_profile_production():
    from google.appengine.api import users
    return users.is_current_user_admin()

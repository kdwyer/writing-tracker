import logging

import webapp2

from jinja2.runtime import TemplateNotFound
from webapp2_extras import auth, sessions, jinja2

from simpleauth import SimpleAuthHandler
import secrets


logger = logging.getLogger(__name__)


class BaseRequestHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)
  
  @webapp2.cached_property    
  def jinja2(self):
    """Returns a Jinja2 renderer cached in the app registry"""
    return jinja2.get_jinja2(app=self.app)
    
  @webapp2.cached_property
  def session(self):
    """Returns a session using the default cookie key"""
    return self.session_store.get_session()
    
  @webapp2.cached_property
  def auth(self):
      return auth.get_auth()
  
  @webapp2.cached_property
  def current_user(self):
    """Returns currently logged in user"""
    user_dict = self.auth.get_user_by_session()
    return self.auth.store.user_model.get_by_id(user_dict['user_id'])
      
  @webapp2.cached_property
  def logged_in(self):
    """Returns true if a user is currently logged in, false otherwise"""
    return self.auth.get_user_by_session() is not None
  
      
  def render(self, template_name, template_vars={}):
    # Preset values for the template
    values = {
      'url_for': self.uri_for,
      'logged_in': self.logged_in,
      'flashes': self.session.get_flashes()
    }
    
    # Add manually supplied template values
    values.update(template_vars)
    
    # read the template or 404.html
    try:
      self.response.write(self.jinja2.render_template(template_name, **values))
    except TemplateNotFound:
      self.abort(404)

  def head(self, *args):
    """Head is used by Twitter. If not there the tweet button shows 0"""
    pass
    
    

class AuthHandler(BaseRequestHandler, SimpleAuthHandler):

    USER_ATTRS = {
      'facebook' : {
        'id'     : lambda id: ('avatar_url', 
          'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
        'name'   : 'name',
        'link'   : 'link'
      },
      'google'   : {
        'picture': 'avatar_url',
        'name'   : 'name',
        'profile': 'link'
      },
      'windows_live': {
        'avatar_url': 'avatar_url',
        'name'      : 'name',
        'link'      : 'link'
      },
      'twitter'  : {
        'profile_image_url': 'avatar_url',
        'screen_name'      : 'name',
        'link'             : 'link'
      },
      'linkedin' : {
        'picture-url'       : 'avatar_url',
        'first-name'        : 'name',
        'public-profile-url': 'link'
      },
      'linkedin2' : {
        'picture-url'       : 'avatar_url',
        'first-name'        : 'name',
        'public-profile-url': 'link'
      },
      'foursquare'   : {
        'photo'    : lambda photo: ('avatar_url', photo.get('prefix') + '100x100' + photo.get('suffix')),
        'firstName': 'firstName',
        'lastName' : 'lastName',
        'contact'  : lambda contact: ('email',contact.get('email')),
        'id'       : lambda id: ('link', 'http://foursquare.com/user/{0}'.format(id))
      },
      'openid'   : {
        'id'      : lambda id: ('avatar_url', '/img/missing-avatar.png'),
        'nickname': 'name',
        'email'   : 'link'
      }
    }

    def _on_signin(self, data, auth_info, provider):
        auth_id = '%s:%s' % (provider, data['id'])
        logger.info('User id could be: <%s>', auth_id)
        logger.info(data)
        logger.info(auth_info)
        user = self.auth.store.user_model.get_by_auth_id(auth_id)
        _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])
        if user:
            logger.info('Found exisiting user to log in.')
            user.populate(**_attrs)
            user.put()
            self.auth.set_session(
                    self.auth.store.user_to_dict(user)
            )
        else:
            if self.logged_in:
                logger.info('Updating currently logged in user.')
                u = self.current_user
                u.populate(**_attrs)
                u.add_auth_id(auth_id)
            else:
                logger.info('Adding  new user.')
                ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
                if ok:
                    self.auth.set_session(self.auth.store.user_to_dict(user))
        self.redirect_to('home')

    def logout(self):
        self.auth.unset_session()
        self.redirect_to('index')

    def _callback_uri_for(self, provider):
        return self.uri_for('auth_callback', provider=provider, _full=True)

    def _get_consumer_info_for(self, provider):
        return secrets.AUTH_CONFIG[provider]

    def _to_user_model_attrs(self, data, attrs_map):
        user_attrs = {}
        for k,v in attrs_map.iteritems():
            attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
            user_attrs.setdefault(*attr)
        return user_attrs

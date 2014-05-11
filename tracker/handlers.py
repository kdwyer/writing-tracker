import logging

from google.appengine.ext import ndb
import webapp2
from webapp2_extras import auth, jinja2

from . import models

logger = logging.getLogger(__file__)


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

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
  
    def render_response(self, _template, **context):
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class Index(BaseHandler):

    def get(self):
        self.render_response('index.html', **{})


class Home(BaseHandler):

    def get(self):
        user = self.current_user if self.logged_in else None
        if user:
            context = {
                    'entries': models.Entry.query(ancestor=user.key),
                    'user': user,
            }
        self.render_response('home.html', **context)


class Confirmation(BaseHandler):

    def get(self):
        key = self.request.GET.get('key')
        entry = ndb.Key(urlsafe=key).get()
        context = {
                'entry': entry
        }
        self.render_response('confirm.html', **context)

class Entry(BaseHandler):

    def post(self):
        date = self.request.POST.get('date')
        word_count = self.request.POST.get('word-count')
        genre = self.request.POST.get('genre')
        notes = self.request.POST.get('notes')
        parent = self.current_user.key
        entry = models.Entry.create(date, word_count, genre, notes, parent)
        self.redirect('/confirm/?key=' + entry.urlsafe())

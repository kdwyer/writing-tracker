import datetime
import logging

from google.appengine.ext import ndb
import webapp2
from webapp2_extras import auth, jinja2

from . import models
from . import utils

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

    def build_context(self):
        user = self.current_user if self.logged_in else None
        if user:
            seven_days_ago = utils.seven_days_before(datetime.date.today())
            words = (models.Entry.query(ancestor=user.key)
                    .filter(models.Entry.date>=seven_days_ago))
            entries = (models.Entry.query(ancestor=user.key)
                    .order(-models.Entry.date))
            context = {
                    'seven_day_count': sum(x.word_count for x in words),
                    'entries': entries,
                    'user': user,
                    'genres': ['Short fiction', 'Novel draft', 'Non-fiction',
                            'Academic writing', 'Blog'],
                    'invalids': [],
            }
        return context

    def get(self):
        self.render_response('home.html', **self.build_context())

    def post(self):
        date = self.request.POST.get('date')
        word_count = self.request.POST.get('word-count')
        genre = self.request.POST.get('genre')
        notes = self.request.POST.get('notes')
        parent = self.current_user.key
        try:
            entry = models.Entry.create(date, word_count, genre, notes, parent)
        except ValueError:
            context = self.build_context()
            context['date'] = date
            context['word_count'] = word_count
            context['selected'] = genre
            context['notes'] = notes
            entry_validation = utils.EntryValidation(self.request.POST)
            context['invalids'] = entry_validation.validate()
            self.render_response('home.html', **context)
            return
        self.redirect_to('confirm', key=entry.urlsafe())


class Confirmation(BaseHandler):

    def get(self):
        key = self.request.GET.get('key')
        user = self.current_user if self.logged_in else None
        entry = ndb.Key(urlsafe=key).get()
        seven_days_ago = utils.seven_days_before(datetime.date.today())
        words = (models.Entry.query(ancestor=user.key)
                .filter(models.Entry.date>=seven_days_ago))
        context = {
                'entry': entry,
                'seven_day_count': sum(x.word_count for x in words),
        }
        self.render_response('confirm.html', **context)

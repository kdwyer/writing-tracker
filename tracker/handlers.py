from google.appengine.ext import ndb
import webapp2
from webapp2_extras import jinja2

from . import models

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class Home(BaseHandler):

    def get(self):
        context = {
                'entries': models.Entry.query().fetch()
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

class Entry(webapp2.RequestHandler):

    def post(self):
        date = self.request.POST.get('date')
        word_count = self.request.POST.get('word-count')
        genre = self.request.POST.get('genre')
        notes = self.request.POST.get('notes')
        entry = models.Entry.create(date, word_count, genre, notes)
        self.redirect('/confirm/?key=' + entry.urlsafe())

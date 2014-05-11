import datetime

from google.appengine.ext import ndb


class Entry(ndb.Model):

    date = ndb.DateProperty()
    word_count = ndb.IntegerProperty()
    genre = ndb.StringProperty()
    notes = ndb.TextProperty()

    @classmethod
    def create(cls, date, word_count, genre, notes, parent):
        date_obj = datetime.date(*map(int, date.split('-')))
        return cls(date=date_obj, word_count=int(word_count), genre=genre, notes=notes, parent=parent).put()

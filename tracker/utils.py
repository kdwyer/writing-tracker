import datetime

def seven_days_before(date):
    return date - datetime.timedelta(days=6)


class EntryValidation(object):

    def __init__(self, post):
        self.post = post
        self._invalids = []

    def validate(self):
        self._validate_date()
        self._validate_word_count()
        return self._invalids

    def _validate_date(self):
        d = 'date'
        try:
            datetime.date( *[int(x) for x in self.post.get(d, '').split('-')])
        except ValueError:
            self._invalids.append(d)
        return

    def _validate_word_count(self):
        wc = 'word-count'
        try:
            int(self.post.get(wc, ''))
        except ValueError:
            self._invalids.append(wc)
        return

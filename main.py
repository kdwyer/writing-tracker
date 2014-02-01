import webapp2

app = webapp2.WSGIApplication([
    (r'/', 'tracker.handlers.Home'),
    (r'/entry/', 'tracker.handlers.Entry'),
    (r'/confirm/.*', 'tracker.handlers.Confirmation'),
    ], debug=True)

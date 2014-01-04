import webapp2

app = webapp2.WSGIApplication([
    (r'/', 'handlers.Home'),
    ], debug=True)

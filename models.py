from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    vnos=ndb.StringProperty()
    avtor=ndb.StringProperty()
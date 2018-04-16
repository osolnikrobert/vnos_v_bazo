#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
from models import Sporocilo
from google.appengine.api import urlfetch

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class VnosHandler(BaseHandler):
    def get(self):
        return self.render_template("vnos.html")

    def post(self):
        v1 = self.request.get("vnos")
        a1 = self.request.get("avtor")

        sporocilo = Sporocilo(vnos=v1, avtor=a1)
        sporocilo.put()

        return self.redirect_to("seznam-tukaj")


class SeznamVnosovHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam.html", params=params)

class UrediVnosHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {"sporocilo": sporocilo}

        return self.render_template("uredi-sporocilo.html", params=params)
    def post(self, sporocilo_id):
        v1 = self.request.get("vnos")
        a1 = self.request.get("avtor")

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.avtor = a1
        sporocilo.vnos = v1
        sporocilo.put()

        params = {"sporocilo": sporocilo}

        return self.redirect_to("seznam-tukaj")

class IzbrisiHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {"sporocilo": sporocilo}

        return self.render_template("izbrisi-sporocilo.html", params=params)

    def post(self, sporocilo_id):

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()

        return self.redirect_to("seznam-tukaj")

class PodatkiHandler(BaseHandler):
    def get(self):
        data = open("people.json", "r").read()
        json_data = json.loads(data)

        params = {"seznam": json_data}

        return self.render_template("prikazi-podatke.html", params=params)

class PodatkiDrugiHandler(BaseHandler):
    def get(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=Ljubljana,slo&units=metric&appid=fa7238d1f3538715243b4653439be822'

        result = urlfetch.fetch(url)

        json_data = json.loads(result.content)

        params = {"vreme": json_data}

        print(params["vreme"])

        return self.render_template("prikazi-druge-podatke.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnos', VnosHandler),
    webapp2.Route('/seznam', SeznamVnosovHandler, name="seznam-tukaj"),
    webapp2.Route('/uredi-sporocilo/<sporocilo_id:\d+>', UrediVnosHandler),
    webapp2.Route('/izbrisi-sporocilo/<sporocilo_id:\d+>', IzbrisiHandler),
    webapp2.Route('/prikazi-podatke', PodatkiHandler),
    webapp2.Route('/prikazi-druge-podatke', PodatkiDrugiHandler),
], debug=True)

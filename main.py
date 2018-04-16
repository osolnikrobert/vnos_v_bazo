#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo


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

class BlogHandler(BaseHandler):
    def post(self):
        kar_smo_vnesli = self.request.get('vneseno_sporocilo')

        params = {
            "ime": "Robert",
            "sporocila":
                [
                    "1. prvo sporocilo",
                    kar_smo_vnesli
                ]
        }

        return self.render_template("blog.html", params=params)

    def get(self):

        params = {
            "ime": "Robert",
            "sporocila":
            [
                "1. prvo sporocilo",
                "2. drugo sporocilo"
            ]
        }

        return self.render_template("blog.html", params=params)

class KalkulatorHandler(BaseHandler):
    def post(self):
        rezultat = self.request.get('vneseno_1stevilo' + 'vneseno_2stevilo')

        params = {
            [
                rezultat
            ]
        }

        return self.render_template("kalkulator.html", params=params)

    def get(self):
        return self.render_template("kalkulator.html")

class BazaHandler(BaseHandler):
    def post(self):
        params = {
        }

        return self.render_template("blog.html", params=params)

    def get(self):

        params = {
            "podatki_iz_baze": Sporocilo.query().fetch()
        }
        return self.render_template("baza.html", params=params)

class VnosHandler(BaseHandler):
    def post(self):
        tisto_kar_smo_vnseli_v_vnos = self.request.get('vnos')
        tisto_kar_smo_vnseli_v_avtor = self.request.get('avtor')

        nov_vnos = Sporocilo(
            vnos=tisto_kar_smo_vnseli_v_vnos,
            avtor=tisto_kar_smo_vnseli_v_avtor
        )
        nov_vnos.put()

        self.redirect("/baza")

    def get(self):

        params = {
        }
        return self.render_template("vnos-v-bazo.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/kalkulator', KalkulatorHandler),
    webapp2.Route('/baza', BazaHandler),
    webapp2.Route('/vnos_v_bazo', VnosHandler),
], debug=True)

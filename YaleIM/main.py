import webapp2
import json
import urllib2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

global scoresjson, matchesjson
scoresjson = {"scores" : {}}
matchesjson   = {"matches" : []}

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
      self.write("Main Page")

class UpdateScoresHandler(Handler):
  def get(self):
      self.render("updateScores.html")
  def post(self):
      scoresjson["scores"]["berkeley"] = self.request.get("berkeley")
      scoresjson["scores"]["branford"] = self.request.get("branford")
      scoresjson["scores"]["calhoun"] = self.request.get("calhoun")
      scoresjson["scores"]["davenport"] = self.request.get("davenport")
      scoresjson["scores"]["erzastiles"] = self.request.get("erzastiles")
      scoresjson["scores"]["johnathanedwards"] = self.request.get("johnathanedwards")
      scoresjson["scores"]["morse"] = self.request.get("morse")
      scoresjson["scores"]["pierson"] = self.request.get("pierson")
      scoresjson["scores"]["saybrook"] = self.request.get("saybrook")
      scoresjson["scores"]["silliman"] = self.request.get("silliman")
      scoresjson["scores"]["timothydwight"] = self.request.get("timothydwight")
      scoresjson["scores"]["trumbull"] = self.request.get("trumbull")

      self.redirect("/")

class UpdateMatchesHandler(Handler):
  def get(self):
      self.render("updateMatches.html")
  def post(self):
      match = {}
      match["team1"] = self.request.get("team1")
      match["team2"] = self.request.get("team2")
      match["date"]  = {"year"  : self.request.get("year"),
                        "month" : self.request.get("month"),
                        "day" : self.request.get("day"),
                        "hour" : self.request.get("hour"),
                        "minutes": self.request.get("minutes")}
      match["sport"] = self.request.get("sport")
      match["location"] = self.request.get("location")

      matchesjson["matches"].append(match)
      self.redirect("/")
      
class ScoresHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(json.dumps(scoresjson))

class MatchesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(json.dumps(matchesjson))

class FlushHandler(webapp2.RequestHandler):
    def get(self):
      global scoresjson, matchesjson
      scoresjson = {"scores": {}}
      matchesjson = {"matches": []}
      self.redirect("/")
      
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/matches', UpdateMatchesHandler),
    ('/scores', UpdateScoresHandler),
    ('/scores.json', ScoresHandler),
    ('/matches.json', MatchesHandler),
    ('/flush', FlushHandler)
], debug=True)


      
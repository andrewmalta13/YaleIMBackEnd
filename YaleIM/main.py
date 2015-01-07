import webapp2
import json
import urllib2
import os
import jinja2
import ast
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)



class Match(db.Model):
  team1 = db.StringProperty(required=True)
  team2 = db.StringProperty(required=True)
  date = db.TextProperty(required=True)
  sport = db.StringProperty(required=True)
  location = db.StringProperty(required=True)

class Team(db.Model):
  college = db.StringProperty(required=True)
  sport = db.StringProperty(required=True)
  email = db.EmailProperty(required=True)
  wins = db.IntegerProperty(required=True)
  losses = db.IntegerProperty(required=True)

class Scores(db.Model):
  scores = db.TextProperty(required=True)
  timeSubmitted = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    #a helper method to parse the datetime-local input string
    #to an array of [year, month, day, hour, minutes]
    def parseDateTime(self, dtstring):
        dtstring = dtstring.replace("T", "-")
        dtstring = dtstring.replace(":", "-")
        return dtstring.split("-")

class MainHandler(Handler):
    def get(self):
      self.write("Main Page")

class UpdateScoresHandler(Handler):
  def get(self):
      self.render("updateScores.html")
  def post(self):

      
      scoresjson = {"scores": {}}
      scoresjson["scores"]["berkeley"] = int(self.request.get("berkeley"))
      scoresjson["scores"]["branford"] = int(self.request.get("branford"))
      scoresjson["scores"]["calhoun"] = int(self.request.get("calhoun"))
      scoresjson["scores"]["davenport"] = int(self.request.get("davenport"))
      scoresjson["scores"]["erzastiles"] = int(self.request.get("erzastiles"))
      scoresjson["scores"]["johnathanedwards"] = int(self.request.get("johnathanedwards"))
      scoresjson["scores"]["morse"] = int(self.request.get("morse"))
      scoresjson["scores"]["pierson"] = int(self.request.get("pierson"))
      scoresjson["scores"]["saybrook"] = int(self.request.get("saybrook"))
      scoresjson["scores"]["silliman"] = int(self.request.get("silliman"))
      scoresjson["scores"]["timothydwight"] = int(self.request.get("timothydwight"))
      scoresjson["scores"]["trumbull"] = int(self.request.get("trumbull"))

      s = Scores(scores = str(scoresjson))
      s.put()

      #self.redirect("/")

class UpdateMatchesHandler(Handler):
  def get(self):
      self.render("updateMatches.html")
  def post(self):
      dateTimeArray = self.parseDateTime(self.request.get("date"))
      dateDict = {"year"  : dateTimeArray[0],
              "month" : dateTimeArray[1],
              "day" : dateTimeArray[2],
              "hour" : dateTimeArray[3],
              "minutes": dateTimeArray[4]}

      match = Match(team1 = self.request.get("team1"), team2 = self.request.get("team2"),
            date  = str(dateDict), sport = self.request.get("sport"), 
            location = self.request.get("location"))

      match.put()

      self.redirect("/matches")

class UpdateTeamsHandler(Handler):
  def get(self):
      self.render("updateTeams.html")
  def post(self):
      team = Team(college = self.request.get("college"), sport = self.request.get("sport"),
        email = self.request.get("email"), wins = int(self.request.get("wins")),
        losses = int(self.request.get("losses")))

      team.put()

      self.redirect("/teams")
      
class ScoresHandler(webapp2.RequestHandler):
    def get(self):
        scores = Scores.all() 

        self.response.out.write(str(scores))
        if scores.count() > 0:
            scores.order("-timeSubmitted")
            self.response.out.write(json.dumps(ast.literal_eval(scores[0].scores)))
        else:
            self.response.out.write(json.dumps("{scores: {}}"))

class MatchesHandler(webapp2.RequestHandler):
    def get(self):
        matches = Match.all()
        matchesjson = {"matches": []}
        
        for match in matches:
            matchesjson["matches"].append({"team1": match.team1,
                                "team2": match.team2,
                                "date": ast.literal_eval(match.date),
                                "sport": match.sport,
                                "location": match.location})

        self.response.out.write(json.dumps(matchesjson))

class TeamsHandler(webapp2.RequestHandler):
    def get(self):
        teams = Team.all()
        teamsjson = {"teams": []}

        for team in teams:
            teamsjson["teams"].append({"college": team.college,
                              "sport": team.sport,
                              "email": team.email,
                              "wins": team.wins,
                              "losses": team.losses})

        self.response.out.write(json.dumps(teamsjson))

class FlushHandler(webapp2.RequestHandler):
    def get(self):
      s = Scores.all()
      m = Match.all()
      t = Team.all()

      for scores in s:
        scores.delete()
      for matches in m:
        matches.delete()
      for teams in t:
        teams.delete()

      self.redirect("/")
      
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/scores', UpdateScoresHandler),
    ('/matches', UpdateMatchesHandler),
    ('/teams', UpdateTeamsHandler),
    ('/scores.json', ScoresHandler),
    ('/matches.json', MatchesHandler),
    ('/teams.json', TeamsHandler),
    ('/flush', FlushHandler)
], debug=True)


      
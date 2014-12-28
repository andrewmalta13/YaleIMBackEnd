
import webapp2
import json
import urllib2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        jsondata ={"scores" : 
                      {"berkeley" : 172, "branford" : 345, "calhoun" : 128, "davenport" : 670,
                       "erzastiles" : 659, "johnathanedwards" : 234, "morse" : 546, "silliman" : 123,
                       "timothydwight" : 782, "trumbull" : 1543},

                  "matches" : 
                      {1 : {"team1" : "berkeley", "team2" : "saybrook", "date" :
                       {"month" : 11, "day" : 13, "hour" : 17, "minutes" : 30},
                        "sport" : "Frisbee", "location" : "IM Fields"},

                       2 : {"team1" : "davenport", "team2" : "timothydwight", "date" :
                       {"month" : 11, "day" : 16, "hour" : 15, "minutes" : 30},
                        "sport" : "Soccer", "location" : "IM Fields"},

                       3 : {"team1" : "silliman", "team2" : "saybrook", "date" :
                       {"month" : 12, "day" : 2, "hour" : 9, "minutes" : 25},
                        "sport" : "Tennis", "location" : "IM Courts"},

                       4 : {"team1" : "pierson", "team2" : "morse", "date" :
                       {"month" : 2, "day" : 25, "hour" : 16, "minutes" : 45},
                        "sport" : "Football", "location" : "IM Fields"},

                       5 : {"team1" : "trumbull", "team2" : "calhoun", "date" :
                       {"month" : 2, "day" : 28, "hour" : 17, "minutes" : 45},
                        "sport" : "Frisbee", "location" : "IM Fields"},

                       6 : {"team1" : "johnathanedwards", "team2" : "timothydwight", "date" :
                       {"month" : 5, "day" : 13, "hour" : 7, "minutes" : 30},
                        "sport" : "Intertube Water Polo", "location" : "IM Pool"}
                      }
                  }
        self.response.out.write(json.dumps(jsondata))
      
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

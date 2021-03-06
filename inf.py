from google.appengine.ext import webapp
from google.appengine.ext import db 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, urlfetch
from google.appengine.ext.webapp import template

from util import tmpl, add_user_to_context
from models import Videos, Twitter, NewsItem, Shout

import cgi

import settings
import urllib
import base64

class MainPage(webapp.RequestHandler):
    def get(self):
        context = { }
        #context = add_user_to_context(context)
        self.response.out.write(
            template.render(tmpl('templates/twitter.html'),
            context ))

import feedparser
from google.appengine.api import urlfetch
import datetime

class TwitterPage(webapp.RequestHandler):
    def get(self):
        t = Twitter.all()[0]
        context = add_user_to_context({'keywords': t.keywords  }) 
        self.response.out.write(
            template.render(tmpl('templates/twitter.html'),
            context ))
 
class MapPage(webapp.RequestHandler):
    def get(self):
        context = { }
        self.response.out.write(
            template.render(tmpl('templates/map.html'),
            context ))

class VideoPage(webapp.RequestHandler):
    def get(self):
        v = Videos.all()[0]
        context = add_user_to_context({ 'users': v.users, 'searches': v.searches  }) 
        self.response.out.write(
            template.render(tmpl('templates/video.html'),
            context ))

class InitData(webapp.RequestHandler):
    def get(self):
        v = Videos(key_name='videos') 
        v.users =  ["ShangoRBG","Halbertis","farhad43","abatebi","iranlover100","SasanShah1","Zendoaut","hadihadithegreat","saeidkermanshah"]
        v.searches = ["iranelection","iran riot","tehran"]
        
        v.put() 
        t = Twitter(key_name='twitter') 
        t.keywords = ['iranelection', 'tehran']
        t.put() 
     

        self.response.out.write('init\'d')

    
class ShoutBox(webapp.RequestHandler): 
     def get(self):
        items = db.GqlQuery("SELECT * FROM Shout ORDER BY date DESC LIMIT 25")
 
        context = add_user_to_context({'shouts':items }) 
        #context = add_user_to_context(context)
        self.response.out.write(
               template.render(tmpl('templates/shoutbox.html'),
               context ))
   

class PostShout(webapp.RequestHandler): 
     def post(self): 
         text = cgi.escape(self.request.get('text')) 
         name = cgi.escape(self.request.get('name')) 
         s = Shout(text=text, name=name)
         s.put() 

         # FIXME 
         apendix = ' #iranelection'
         chars = 140 - len(apendix) 
           
         from secretsettings import twitter_password, twitter_username  
         payload= {'status' : text[:chars] + apendix,  'source' : "iranbreakingnews"}
         payload= urllib.urlencode(payload)
         base64string = base64.encodestring('%s:%s' % (twitter_username, twitter_password))[:-1]
         headers = {'Authorization': "Basic %s" % base64string} 
         url = "http://twitter.com/statuses/update.xml"
         result = urlfetch.fetch(url, payload=payload, method=urlfetch.POST, headers=headers)


         self.redirect('/shoutbox/')

     def get(self):
         self.redirect('/shoutbox/')


application = webapp.WSGIApplication(
   [
    ('/', TwitterPage ),
    ('/twitter/', TwitterPage),
    ('/map/', MapPage), 
    ('/videos/', VideoPage), 
    #('/gnarf/', InitData), 
    ('/shoutbox/', ShoutBox), 
    ('/shoutbox/post/', PostShout), 


   ], debug=True)







def main():
   run_wsgi_app(application)

if __name__ == "__main__":
  main()

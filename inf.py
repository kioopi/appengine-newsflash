from google.appengine.ext import webapp
from google.appengine.ext import db 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

from util import tmpl
from models import Videos, Twitter

# http://pipes.yahoo.com/pipes/pipe.run?_id=UN2R8yBb3hG1Bk05fKAMnA&_render=rss

class MainPage(webapp.RequestHandler):
    def get(self):
        context = { }
        #context = add_user_to_context(context)
        self.response.out.write(
            template.render(tmpl('templates/twitter.html'),
            context ))

#import feedparser
from google.appengine.api import urlfetch
class NewsPage2(webapp.RequestHandler):
    def get(self):
        
        url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=UN2R8yBb3hG1Bk05fKAMnA&_render=rss'
        json = urlfetch.fetch(feed) 
        context = { }
        #context = add_user_to_context(context)
        self.response.out.write(
            template.render(tmpl('templates/news2.html'),
            context ))

class NewsJson(webapp.RequestHandler): 
    def get(self):  
        url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=UN2R8yBb3hG1Bk05fKAMnA&_render=json'
        result = urlfetch.fetch(url) 
        if result.status_code == 200:
            self.response.out.write(result.content) 
        else: 
            self.response.out.write('err') 


class TwitterPage(webapp.RequestHandler):
    def get(self):
        t = Twitter.all()[0]
        context = {'keywords': t.keywords  }
        #context = add_user_to_context(context)
        self.response.out.write(
            template.render(tmpl('templates/twitter.html'),
            context ))

class NewsPage(webapp.RequestHandler):
    def get(self):
        context = { }
        #context = add_user_to_context(context)
        self.response.out.write(
            template.render(tmpl('templates/news.html'),
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
        context = { 'users': v.users, 'searches': v.searches  }
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

    



application = webapp.WSGIApplication(
   [
    ('/', MainPage),
    ('/twitter/', TwitterPage),
    ('/news/', NewsPage), 
    ('/news.json', NewsJson), 
    ('/map/', MapPage), 
    ('/videos/', VideoPage), 
    #('/gnarf/', InitData), 

   ], debug=True)







def main():
   run_wsgi_app(application)

if __name__ == "__main__":
  main()

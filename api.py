from google.appengine.ext import webapp
from google.appengine.ext import db 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

from util import tmpl
from models import Videos, Twitter, NewsItem

import settings

from google.appengine.api import urlfetch

class GetNews(webapp.RequestHandler):
    def get(self): 
         # takes a date as parameter and returns news items later than that as json
        pass

class PostNews(webapp.RequestHandler): 
    def post(self): 
        # takes news dataset and adds it to the db
        pass

class Vote(webapp.RequestHandler): 
    def post(self): 
        # takes a NewsItem key and adds the loggeg-in user to votes
        # returns the news object with the updated vote count ?
        pass


class MainPage(webapp.RequestHandler):
    def get(self):
        context = { }
        #context = add_user_to_context(context)
        self.response.out.write(
            template.render(tmpl('templates/twitter.html'),
            context ))
class NewsJson(webapp.RequestHandler): 
    def get(self):  
        url = settings.YAHOO_PIPE % 'json' 
        result = urlfetch.fetch(url) 
        if result.status_code == 200:
            # FIXME this needs the proper mime
            self.response.out.write(result.content) 
        else: 
            self.response.out.write('err') 

    

application = webapp.WSGIApplication(
   [
    ('/', NewsPage),
    ('/news/', GetNews), 
    ('/allnews', NewsJson), 
   ], debug=True)







def main():
   run_wsgi_app(application)

if __name__ == "__main__":
  main()

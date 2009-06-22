from google.appengine.ext import webapp
from google.appengine.ext import db 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

from util import tmpl
from models import Videos, Twitter, NewsItem

import settings

from google.appengine.labs.api import urlfetch

import cgi 

class GetNews(webapp.RequestHandler):
    def get(self): 
         # takes a date as parameter and returns news items later than that as json
        pass
        

class PostNews(webapp.RequestHandler): 
    def post(self): 
        # takes news dataset and adds it to the db
        pass

class Bump(webapp.RequestHandler): 
    def post(self): 
        # takes a NewsItem key and adds the loggeg-in user to votes
        # returns the news object with the updated vote count ?
        user = users.get_current_user()
        if user: 
            key = cgi.escape(self.request.get('key'))
            if key: 
                item = NewsItem.get_by_key_name(key)  
                if user not in item.bumps: 
                    item.bumps.append(user)
                    item.put()  
                    self.response.out.write(item.key().name())

        else:
            self.error(401) 

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
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(result.content) 
        else: 
            self.response.out.write('err') 

    

application = webapp.WSGIApplication(
   [
    ('/api/news/', GetNews), 
    ('/api/bump/', Bump), 
    ('/api/allnews', NewsJson), 
   ], debug=True)







def main():
   run_wsgi_app(application)

if __name__ == "__main__":
  main()

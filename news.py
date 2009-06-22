from google.appengine.ext import webapp
from google.appengine.ext import db 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, urlfetch
from google.appengine.ext.webapp import template

from util import tmpl, add_user_to_context
from models import Videos, Twitter, NewsItem, Shout

import cgi

import settings
import feedparser
from google.appengine.api import urlfetch
import datetime

class FetchNews(webapp.RequestHandler): 
    def get(self): 
        url = settings.YAHOO_PIPE % 'rss'  
        result = urlfetch.fetch(url) 
        if result.status_code == 200:
            feed = feedparser.parse(result.content) 
            for i in feed.entries:  
                item = NewsItem(key_name=i.guid) 
                item.url = i.link
                item.title = i.title 
                item.text = i.summary
                item.date = datetime.datetime(*i.date_parsed[:6])
                item.orderdate = datetime.datetime(*i.date_parsed[:6])
                item.put() 

            items = db.GqlQuery("SELECT * FROM NewsItem ORDER BY orderdate DESC LIMIT 100")
 
            context = {'news':items }
            #context = add_user_to_context(context)
            self.response.out.write(
               template.render(tmpl('templates/news2.html'),
               context ))
        else: 
            self.response.out.write('err') 

class NewsJson(webapp.RequestHandler): 
    def get(self):  
        url = settings.YAHOO_PIPE % 'json' 
        result = urlfetch.fetch(url) 
        if result.status_code == 200:
            # FIXME this needs the proper mime
            self.response.out.write(result.content) 
        else: 
            self.response.out.write('err') 



class NewsPage(webapp.RequestHandler):
    def get(self):
        items = db.GqlQuery("SELECT * FROM NewsItem ORDER BY date DESC LIMIT 25")
 
        context = add_user_to_context({'news':items }) 
        #context = add_user_to_context(context)
        self.response.out.write(
               template.render(tmpl('templates/news2.html'),
               context ))
 

application = webapp.WSGIApplication(
   [
    ('/news/', NewsPage), 
    ('/news.json', NewsJson), 
   ], debug=True)



def main():
   run_wsgi_app(application)

if __name__ == "__main__":
  main()

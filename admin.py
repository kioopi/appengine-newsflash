from google.appengine.ext import webapp
from google.appengine.ext import db 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

from util import tmpl, add_user_to_context
from models import Videos, Twitter, NewsItem, NewsFeed

import settings

import feedparser

from google.appengine.api import urlfetch

import cgi 


from google.appengine.api.labs import taskqueue


"""Load custom Django template filters"""
webapp.template.register_template_library('templatetags.customfilters')

class NewsFeeds(webapp.RequestHandler):
    def get(self): 
        items = db.GqlQuery("SELECT * FROM NewsFeed ORDER BY date DESC LIMIT 25")

        context = add_user_to_context({'feeds':items })
        #context = add_user_to_context(context)
        self.response.out.write(
               template.render(tmpl('templates/admin/feeds.html'),
               context ))

class PostFeed(webapp.RequestHandler):
     def post(self):
         text = cgi.escape(self.request.get('text'))
         url = cgi.escape(self.request.get('url'))
         f = NewsFeed(url=url, name=name)
         f.put()
         
         taskqueue.add(queue_name='fetch-news-queue', url='/admin/feeds/fetch/', params={'key':f.key})

         self.redirect('/admin/feeds/')

     def get(self):
         self.redirect('/admin/feeds/')

class FeedPreview(webapp.RequestHandler): 
    def get(self):     
        url = cgi.escape(self.request.get('url'))
        if not url: 
           self.response.out.write('Please pass a feed-url as a get-param "url".')
        try: 
           result = urlfetch.fetch(url)
        except: 
           self.response.out.write('Invalid or non-existing URL.')
            
        
        if result.status_code == 200:
            rssfeed = feedparser.parse(result.content)
            self.response.out.write(
               template.render(tmpl('templates/admin/feedpreview.html'),
               {'feed': rssfeed} ))
        else:  
            self.response.out.write('error') 
 
            
        
  
class FetchFeed(webapp.RequestHandler): 
     def post(self):
         key = self.request.get('key')
         feed = NewsFeed.get_by_key_name(key)
         # FIXME check if feed was retrieved
         result = urlfetch.fetch(feed.url)
         if result.status_code == 200:
             rssfeed = feedparser.parse(result.content)
             for i in rssfeed.entries:
                 item = NewsItem(key_name=i.guid)
                 item.url = i.link
                 item.title = i.title
                 item.text = i.summary
                 item.date = datetime.datetime(*i.date_parsed[:6])
                 item.orderdate = datetime.datetime(*i.date_parsed[:6])
                 item.source = feed
                 item.put()
             feed.last_fetch = datetime.datetime.now() 
             feed.put() 
             taskqueue.add(queue_name='fetch-news-queue', url='/admin/feeds/fetch/', params={'key':feed.key})
             self.response.out.write('feed pulled')
         else:  
             self.error(500)
             
         


         
application = webapp.WSGIApplication(
   [
    ('/admin/', NewsFeeds), 
    ('/admin/feeds/', NewsFeeds), 
    ('/admin/feeds/post/', PostFeed), 
    ('/admin/feeds/preview/', FeedPreview), 
    ('/admin/feeds/fetch/', PostFeed), 
   ], debug=True)







def main():
   run_wsgi_app(application)

if __name__ == "__main__":
  main()

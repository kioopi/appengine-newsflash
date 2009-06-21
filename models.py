from google.appengine.ext import db
from google.appengine.api import users


class Videos(db.Model): 
    users = db.StringListProperty() 
    searches = db.StringListProperty() 


class Twitter(db.Model): 
    keywords = db.StringListProperty() 


class NewsFeed(db.Model): 
    name = db.StringProperty() 
    last_fetch = db.DateTimeProperty()  
    url = db.LinkProperty()
    active = db.BooleanProperty(default=True) 


class NewsItem(db.Model):
    url = db.LinkProperty()

    title = db.StringProperty() 
    text = db.TextProperty() 
    date = db.DateTimeProperty()  

    orderdate = db.DateTimeProperty() 

    bumps = db.ListProperty(users.User)
    sages = db.ListProperty(users.User)

    source = db.ReferenceProperty(NewsFeed) 

    def bumpyness(self): 
        return len(self.bumps) - len(self.sages) 

    
class Shout(db.Model): 
    date = db.DateTimeProperty(auto_now_add=True)  
    text = db.TextProperty() 
    name = db.StringProperty() 


class Comment(db.Model):
    newsitem_url = db.LinkProperty()

    newsitem = db.ReferenceProperty(NewsItem)


    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    

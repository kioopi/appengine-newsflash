from google.appengine.ext import db
from google.appengine.api import users


class Videos(db.Model): 
    users = db.StringListProperty() 
    searches = db.StringListProperty() 


class Twitter(db.Model): 
    keywords = db.StringListProperty() 



class NewsItem(db.Model):
    url = db.LinkProperty()

    title = db.StringProperty() 
    text = db.TextProperty() 
    date = db.DateTimeProperty()  


    votes = db.ListProperty(users.User)


class Comment(db.Model):
    newsitem_url = db.LinkProperty()

    newsitem = db.ReferenceProperty(NewsItem)


    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    

from google.appengine.ext import db


class Videos(db.Model): 
    users = db.StringListProperty() 
    searches = db.StringListProperty() 


class Twitter(db.Model): 
    keywords = db.StringListProperty() 

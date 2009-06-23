from google.appengine.ext import webapp
import datetime 

register = webapp.template.create_template_register()

def feedparsed_date(value): 
    return datetime.datetime( *value[:6] )
register.filter(feedparsed_date)

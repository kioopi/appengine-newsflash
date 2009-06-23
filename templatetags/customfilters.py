from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def feedparsed_date(value, arg): 
    return datetime.datetime( *value[:6] )
register.filter(feedparsed_date)

import os 

def tmpl(name): return os.path.join(os.path.dirname(__file__),  name)

def add_user_to_context(context={}):
    """Takes a dictionary and add a key user to it if a user is logged in.
       Otherwise it adds a key loginurl.

       Returns the altered dictionary."""
    from google.appengine.api import users
    user = users.get_current_user()
    if user:
         context['user'] = user
         context['logouturl'] = users.create_logout_url("/")
         if users.is_current_user_admin(): 
             context['admin'] = True
    else:
         context['loginurl'] = users.create_login_url("/")
    return context




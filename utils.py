import os
import re
import hashlib
import hmac
import random
import jinja2
import time
from string import letters
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

SECRET = "g8ccfgjUZrR6iqhsUMd"


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# get the key from blog table
def blog_key(name='default'):
    return db.Key.from_path('Blog', name)


# get the key from User table
def users_key(group='default'):
    return db.Key.from_path('users', group)


def make_salt():
    return ''.join(random.choice(letters) for x in xrange(5))


def make_pw_hash(name, pwd, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pwd + salt).hexdigest()
    return "%s|%s" % (salt, h)


def valid_pw(name, pwd, h):
    salt = h.split("|")[0]
    return h == make_pw_hash(name, pwd, salt)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(SECRET, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split("|")[0]
    if secure_val == make_secure_val(val):
        return val


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    PWD_RE = re.compile(r"^.{3,20}$")
    return password and PWD_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+[\S]+.[\S]+$")
    return email and EMAIL_RE.match(email)


def login_required(func):
    """
    A decorator to confirm a user is logged in or redirect as needed.
    """
    def login(self, *args, **kwargs):
        # Redirect to login if user not logged in, else execute func.
        if not self.user:
            self.redirect("/login")
        else:
            func(self, *args, **kwargs)
    return login

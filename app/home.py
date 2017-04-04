from google.appengine.ext import db
from handler import Handler
from utils import *


class MainPage(Handler):

    def get(self):
        # get all blog posts
        posts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")

        self.render("./blog/home.html", posts=posts)

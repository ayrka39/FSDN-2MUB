from google.appengine.ext import db
from models.post import Blog
from models.user import User


class Comment(db.Model):
    post = db.ReferenceProperty(Blog, required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    text = db.TextProperty(required=True)

    @classmethod
    def count_by_blog_id(cls, blog_id):
        """ get number of comments for a blog id """
        c = Comment.all().filter('post =', blog_id)
        return c.count()

    @classmethod
    def all_by_blog_id(cls, blog_id):
        """ get all comments for a specific blog id """
        c = Comment.all().filter('post =', blog_id).order('created')
        return c

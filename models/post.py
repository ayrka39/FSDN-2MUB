from google.appengine.ext import db
from utils import *
from models.user import User


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User,
                                required=True,
                                collection_name="blogs")

    # show line breaks in blog content correctly when page is rendered
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("./blog/blogpost.html", post=self)

    @classmethod
    def by_id(cls, uid):
        return Post.get_by_id(uid, parent=blog_key())

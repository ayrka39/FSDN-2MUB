import webapp2
from app.home import MainPage
from app.account import Register
from app.access import Login
from app.access import Logout
from app.newpost import NewPost
from app.blogpost import BlogPost
from app.blogpost import DeletePost
from app.blogpost import EditPost
from app.comment import DeleteComment
from app.comment import EditComment

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/post/([0-9]+)', BlogPost),
    ('/login', Login),
    ('/logout', Logout),
    ('/signup', Register),
    ('/edit/([0-9]+)', EditPost),
    ('/delete/([0-9]+)', DeletePost),
    ('/blog/([0-9]+)/editcomment/([0-9]+)', EditComment),
    ('/blog/([0-9]+)/deletecomment/([0-9]+)', DeleteComment),
], debug=True)

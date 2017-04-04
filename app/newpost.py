from handler import Handler
from utils import *
from models.post import Blog
from models.user import User


class NewPost(Handler):

    @login_required
    def get(self):
        self.render("./blog/newpost.html")

    @login_required
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content").replace('\n', '<br>')
        user_id = User.by_name(self.user.name)

        if subject and content:
            a = Blog(
                parent=blog_key(),
                subject=subject,
                content=content,
                user=user_id)
            a.put()
            time.sleep(0.1)
            self.redirect('/')

        elif self.request.get("cancel"):
            self.redirect('/')

        else:
            post_error = "No blank fields, please!"
            self.render(
                "./blog/newpost.html",
                subject=subject,
                content=content,
                post_error=post_error)

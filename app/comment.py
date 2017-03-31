from google.appengine.ext import db
from handler import Handler
from utils import *
from models.post import Blog
from models.comment import Comment


class DeleteComment(Handler):

    def get(self, post_id, comment_id):
        # get the comment from the comment id
        comment = Comment.get_by_id(int(comment_id))
        # check if there is a comment associated with that id
        if comment:
            # check if this user is the author of this comment
            if comment.user.name == self.user.name:
                # delete the comment and redirect to the post page
                db.delete(comment)
                time.sleep(0.1)
                self.redirect('/post/%s' % str(post_id))
            
            else:
                self.write("You can only delete your comments")


class EditComment(Handler):

    def get(self, post_id, comment_id):
        # get the blog and comment from blog id and comment id
        post = Blog.get_by_id(int(post_id), parent=blog_key())
        comment = Comment.get_by_id(int(comment_id))
        # check if there is a comment associated with that id
        if comment and comment.user.name == self.user.name:
            self.render("./comment/editcomment.html", comment_text=comment.text)
            
        else:
            error = "You can only edit your comments'"
            self.render("./comment/editcomment.html", edit_error=error)

    def post(self, post_id, comment_id):
        # if the user clicks on update comment
        if self.request.get("update_comment"):
            # get the comment for that comment id
            comment = Comment.get_by_id(int(comment_id))
            
            if comment.user.name == self.user.name:
                # update the text of the comment and redirect to the post page
                comment.text = self.request.get('comment_text')
                comment.put()
                time.sleep(0.1)
                self.redirect('/post/%s' % str(post_id))
                
            else:
                error = "You cannot edit other users' comments'"
                self.render(
                    "./comment/editcomment.html",
                    comment_text=comment.text,
                    edit_error=error)

from google.appengine.ext import db
from handler import Handler
from utils import *
from models.post import Blog
from models.comment import Comment
from models.like import Like
from models.user import User


class BlogPost(Handler):

    def get(self, blog_id):
        # get the key for the blog post
        key = db.Key.from_path("Blog", int(blog_id), parent=blog_key())
        post = db.get(key)

        likes = Like.by_blog_id(post)
        post_comments = Comment.all_by_blog_id(post)
        comments_count = Comment.count_by_blog_id(post)

        self.render(
            "./blog/blogpost.html",
            post=post,
            likes=likes,
            post_comments=post_comments,
            comments_count=comments_count)

    def post(self, blog_id):
        # get all the necessary parameters
        key = db.Key.from_path("Blog", int(blog_id), parent=blog_key())
        post = db.get(key)
        user_id = User.by_name(self.user.name)
        comments_count = Comment.count_by_blog_id(post)
        post_comments = Comment.all_by_blog_id(post)
        likes = Like.by_blog_id(post)
        previously_liked = Like.check_like(post, user_id)

        # check if the user is logged in
        if self.user:
            # if the user clicks on like
            if self.request.get("like"):
                # first check if the user is trying to like his own post
                if post.user.key().id() != User.by_name(self.user.name).key().id():
                    # then check if the user has liked this post before
                    if previously_liked == 0:
                        # add like to the likes database and refresh the page
                        l = Like(
                            post=post, user=User.by_name(
                                self.user.name))
                        l.put()
                        time.sleep(0.1)
                        self.redirect('/post/%s' % str(post.key().id()))

                    else:
                        error = "You have already liked this post"
                        self.render(
                            "./blog/blogpost.html",
                            post=post,
                            likes=likes,
                            error=error,
                            comments_count=comments_count,
                            post_comments=post_comments)

                else:
                    error = "You cannot like your own posts"
                    self.render(
                        "./blog/blogpost.html",
                        post=post,
                        likes=likes,
                        error=error,
                        comments_count=comments_count,
                        post_comments=post_comments)
           
            # if the user clicks on add comment get the comment text first
            if self.request.get("add_comment"):
                comment_text = self.request.get("comment_text")
                # check if there is anything entered in the comment text area
                if comment_text:
                    # add comment to the comments database and refresh page
                    c = Comment(
                        post=post, user=User.by_name(
                            self.user.name), text=comment_text)
                    c.put()
                    time.sleep(0.1)
                    self.redirect('/post/%s' % str(post.key().id()))

                else:
                    comment_error = "Please enter a comment in the text area to post"
                    self.render(
                        "./blog/blogpost.html",
                        post=post,
                        likes=likes,
                        comments_count=comments_count,
                        post_comments=post_comments,
                        comment_error=comment_error)
           
        # otherwise if the user is not logged in take them to the login page
        else:
            self.redirect("/login")


class DeletePost(Handler):

    def get(self, blog_id):
        key = db.Key.from_path("Blog", int(blog_id), parent=blog_key())
        post = db.get(key)

        # check if this user is the author of this post
        if post.user.key().id() == User.by_name(self.user.name).key().id():
            db.delete(key)
            time.sleep(0.1)
            self.redirect('/') 

        else:
            self.redirect("/login")


class EditPost(Handler):

    def get(self, blog_id):
        key = db.Key.from_path("Blog", int(blog_id), parent=blog_key())
        post = db.get(key)

        # check if the user is logged in
        if self.user:
            # check if this user is the author of this post
            if post.user.key().id() == User.by_name(self.user.name).key().id():
                self.render("./blog/editpost.html", post=post)
            
            else:
                self.response.out.write("You cannot edit other user's posts")
        
        else:
            self.redirect("/login")

    def post(self, blog_id):

        key = db.Key.from_path("Blog", int(blog_id), parent=blog_key())
        post = db.get(key)

        # if the user clicks on update comment
        if self.request.get("update"):

            # get the subject, content and user id when the form is submitted
            subject = self.request.get("subject")
            content = self.request.get("content").replace('\n', '<br>')

            if post.user.key().id() == User.by_name(self.user.name).key().id():
                # check if both the subject and content are filled
                if subject and content:
                    # update the blog post and redirect to the post page
                    post.subject = subject
                    post.content = content
                    post.put()
                    time.sleep(0.1)
                    self.redirect('/post/%s' % str(blog_id))
            
                else:
                    post_error = "No black fields, please!"
                    self.render(
                        "./blog/editpost.html",
                        subject=subject,
                        content=content,
                        post_error=post_error)

            else:
                self.response.out.write("You can only edit your own posts.")

            
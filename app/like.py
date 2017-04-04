from google.appengine.ext import db
from handler import Handler
from utils import *
from models.post import Blog
from models.comment import Comment
from models.like import Like
from models.user import User


class AddLike(Handler):

    @login_required
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

    @login_required
    def post(self, blog_id):
        # get all the necessary parameters
        key = db.Key.from_path("Blog", int(blog_id), parent=blog_key())
        post = db.get(key)
        user_id = User.by_name(self.user.name)
        comments_count = Comment.count_by_blog_id(post)
        post_comments = Comment.all_by_blog_id(post)
        likes = Like.by_blog_id(post)
        previously_liked = Like.check_like(post, user_id)

        # if the user clicks on like
        if self.request.get("like"):
            # first check if the user is trying to like his own post
            if post.user.key().id() != user_id.key().id():
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

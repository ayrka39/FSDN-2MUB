from utils import *
from handler import Handler
from models.user import User


class Signup(Handler):

    def get(self):
        self.render("./account/signup.html")

    def post(self):
        have_error = False
        # get the username, password, verify and emails field that the user
        # entered
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        # if the username is not valid throw an error
        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        # if the password is not valid through an error
        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        # if the password and verify password don't match throw an error
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords do not match."
            have_error = True

        # if we have an error render the page with the error and keep the
        # entered values
        if have_error:
            self.render("./account/signup.html", **params)

        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):

    def done(self):
        # check if the username already exists
        u = User.by_name(self.username)
        # if the username already exists throw an error
        if u:
            error = 'That user already exists.'
            self.render('./account/signup.html', error_username=error)

        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')

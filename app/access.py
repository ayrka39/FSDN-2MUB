from handler import Handler
from models.user import User
from utils import *


class Login(Handler):

    def get(self):
        self.render('./account/login.html')

    def post(self):
        # get the username and password entered by the user
        username = self.request.get('username')
        password = self.request.get('password')

        # get the user account associated with that username and password
        u = User.login(username, password)

        # if there is a user account associated with that username and password
        if u:
            # login and redirect to the welcome page
            self.login(u)
            self.redirect('/')

        else:
            error = 'Invalid login'
            self.render('./account/login.html', error=error)

class Logout(Handler):

    def get(self):
        # check is the user is logged in
        if self.user:
            # logout the user and take the user to the signup page
            self.logout()
            self.redirect("/")

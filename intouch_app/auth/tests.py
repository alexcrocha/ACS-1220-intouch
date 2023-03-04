# Create your tests here.
import os
from unittest import TestCase
import app

from intouch_app.extensions import app, db, bcrypt
from intouch_app.models import User

"""
Run these tests with the command:
python -m unittest intouch_app.auth.tests
"""

#################################################
# Setup
#################################################


def create_user():
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="me1", password=password_hash)
    db.session.add(user)
    db.session.commit()


#################################################
# Tests
#################################################


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {"username": "Rocky", "password": "Balboa"}
        self.app.post("/signup", data=post_data)
        created_user = User.query.filter_by(username="Rocky").first()
        self.assertIsNotNone(created_user)

    def test_login_correct_password(self):
        create_user()
        self.app.post("/login", data={"username": "me1", "password": "password"})
        response = self.app.get("/")
        response_text = response.get_data(as_text=True)
        self.assertNotIn("Log In", response_text)

    def test_login_nonexistent_user(self):
        response = self.app.post(
            "/login", data={"username": "thisuserdoesnotexist", "password": "password"}
        )
        self.assertIn(
            "No user with that username. Please try again.",
            response.get_data(as_text=True),
        )

    def test_login_incorrect_password(self):
        create_user()
        response = self.app.post(
            "/login", data={"username": "me1", "password": "incorrectpassword"}
        )
        self.assertIn("Please try again.", response.get_data(as_text=True))

    def test_logout(self):
        create_user()
        self.app.post("/login", data={"username": "me1", "password": "password"})
        self.app.get("/logout")
        response = self.app.get("/")
        self.assertIn("login", response.get_data(as_text=True))

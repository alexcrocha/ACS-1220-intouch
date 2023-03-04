# Create your tests here.
import os
import unittest
import app

from datetime import date
from intouch_app.extensions import app, db, bcrypt
from intouch_app.models import Contact, Note, User

"""
Run these tests with the command:
python -m unittest intouch_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_contacts():
    c1 = Contact(
        name='Peter Parker',
        user_id=1
    )
    db.session.add(c1)
    n1 = Note(
        note='Peter Parker is Spiderman',
        created_on=date(2019, 1, 1),
        contact_id=1)
    db.session.add(n1)

    c2 = Contact(
        name='Mary Jane',
        user_id=1
    )
    db.session.add(c2)
    n2 = Note(
        note='Mary Jane is Spiderman\'s girlfriend',
        created_on=date(2019, 1, 1),
        contact_id=2)
    db.session.add(n2)

    db.session.commit()



def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################
class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the contacts dot not show up on the homepage."""
        # Set up
        create_user()
        create_contacts()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        self.assertNotIn('Peter Parker', response_text)
        self.assertNotIn('Mary Jane', response_text)
        self.assertNotIn('me1', response_text)
        self.assertNotIn('Add Contact', response_text)

    def test_homepage_logged_in(self):
        """Test that the contacts show up on the homepage."""
        # Set up
        create_user()
        create_contacts()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Peter Parker', response_text)
        self.assertIn('Mary Jane', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Add Contact', response_text)
        self.assertIn('Log Out', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_book_detail_logged_out(self):
        """Test that the book does not appear on its detail page."""
        create_user()
        create_contacts()

        response = self.app.get('/contact/1', follow_redirects=True)
        # self.assertEqual(response.status_code, 302)

        response_text = response.get_data(as_text=True)
        self.assertIn("Please log in to access this page", response_text)
        self.assertIn("Log In", response_text)

        self.assertNotIn("Peter Parker", response_text)

    def test_book_detail_logged_in(self):
        """Test that the book does not appear on its detail page."""
        create_user()
        create_contacts()
        login(self.app, 'me1', 'password')

        response = self.app.get('/contact/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("Peter Parker", response_text)
        self.assertIn("Log Out", response_text)
        self.assertIn("Spiderman", response_text)

        self.assertNotIn("Please log in to access this page", response_text)
        self.assertNotIn("Log In", response_text)

    def test_update_contact(self):
        """Test updating a contact."""
        # Set up
        create_user()
        create_contacts()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Miles Morales',
            'user_id':1,
        }
        self.app.post('/contact/1', data=post_data)

        contact = Contact.query.get(1)
        self.assertEqual(contact.name, 'Miles Morales')
        self.assertEqual(contact.user_id, 1)

    def test_create_contact(self):
        """Test creating a contact."""
        # Set up
        create_contacts()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Gwen Stacy',
            'user_id':1,
        }
        self.app.post('/create_contact', data=post_data)


        created_contact = Contact.query.filter_by(name='Gwen Stacy').one()
        self.assertIsNotNone(created_contact)
        self.assertEqual(created_contact.name, 'Gwen Stacy')
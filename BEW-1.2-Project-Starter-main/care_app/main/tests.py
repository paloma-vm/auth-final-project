# Create your tests here.
import os
import unittest
import app

from datetime import date, datetime
from flask_login import current_user
from care_app.extensions import app, db, bcrypt
from care_app.models import User, Client, Activity, Message


# """To run these tests, use python3 -m unittest discover"""
"""To run these tests, use python3 -m unittest care_app.main.tests"""


# SETUP-----------------------------------------------------------------------
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_users():
 # Creates a user with username 'Myname' and password of '123456'
    password_hash = bcrypt.generate_password_hash('123456').decode('utf-8')
    user_1 = User(username='Myname', password=password_hash)
    user_2 = User(username='Othername', password=password_hash)

    # user_1 = User(username='Myname', password=password_hash, first_name='Some', last_name='Person')
    # user_2 = User(username='Othername', password=password_hash, first_name='Other', last_name='Human')

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()
    

def create_client():
    client_1 = Client(
        first_name='Mommy', 
        last_name='Dearest', 
        room_number=1234, 
        date_of_birth=date(1940, 6, 12), # SQLite Date type only accepts Python date objects as input
        diet='VEGAN', 
        start_date=date(2020, 3, 15)
    )
    db.session.add(client_1)
    db.session.commit()


# def create_message():
#     message_1 = Message(
#         to=user_2
#     )

# TESTS --------------------------------------
class MainTests(unittest.TestCase):
    """Tests for main"""
# from testing homework
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_home_logged_out(self):
        # set up
        create_users()
        create_client()

        # scenario
        """Test that the homepage shows 'The bridge between family and caregiver.' """
        response = self.app.get('/', follow_redirects=True)
        # check status code
        self.assertEqual(response.status_code, 200)
        # actual result
        response_text = response.get_data(as_text=True)
        # expected result
        
        self.assertIn('The bridge between family and caregiver.', response_text)
        self.assertNotIn('New Client', response_text)
        
    def test_home_logged_in(self):
        # set up
        create_users()
        login(self.app, 'Myname', '123456')

        # scenario
        """Test that the homepage shows 'You are logged in as' """
        response = self.app.get('/', follow_redirects=True)
        # check status code
        self.assertEqual(response.status_code, 200)
        # actual result
        response_text = response.get_data(as_text=True)
        # expected result
        
        self.assertIn('You are logged in as', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_create_client_logged_in(self):
        # set up
        create_users()
        login(self.app, 'Myname', '123456')

        # scenario
        """Test creating a client while logged in"""
        # make a POST request with data
        post_data = {
            'first_name': 'Joe',
            'last_name': 'Smith',
            'room_number': 1234,
            'date_of_birth': date(1945, 3, 25),
            'diet': 'VEGAN',
            'start_date': date(2021, 2, 15)
        }
        self.app.post('/create-client', data=post_data)
       
        # make sure the client was actually created
        created_client = Client.query.filter_by(first_name='Joe').one()
        self.assertIsNotNone(created_client)
        self.assertEqual(created_client.room_number, 1234)

    def test_create_client_logged_out(self):
        # set up
        create_users()

        # scenario
        """Test creating a client while logged out"""
        # make a GET request
        response = self.app.get('/create-client')
       
        # make sure the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('login?next=%2Fcreate-client', response.location)

# I am writing this test in an attempt to solve the issues with create-message
    def test_create_message_logged_in(self):
        # set up
        create_users()
        login(self.app, 'Myname', '123456')

        # scenario
        """Test creating a message while logged in """
        # make a POST request with data
        post_data = {
            'to': 'user_1',
            'subject': 'bus trip',
            'message_body': 'Join us today!',
            'photo_url': '',
            'sender_id': current_user.id,
            'sender': current_user,
            'timestamp': datetime.now().strftime('%A, %B %d, %Y, %H:%M')
        }
        self.app.post('/create-message', data=post_data)
       
        # make sure the message was actually created
        created_message = Message.query.filter_by(subject='bus trip').one()
        self.assertIsNotNone(created_message)
        self.assertEqual(created_message.photo_url, '')

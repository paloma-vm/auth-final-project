"""create db models to represent tables"""
from care_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to use enums with forms"""
    @classmethod
    def choices(cls):
        return[(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Diet(FormEnum):
    NO_RESTRICTIONS = 'No Dietary Restrictions'
    DIABETIC = 'Diabetic'
    GLUTEN_FREE = 'Gluten Free'
    VEGETARIAN = 'Vegetarian'
    VEGAN = 'Vegan'
    LOW_SODIUM = 'Low Sodium'
    LACTOSE_INTOLERANT = 'Lactose Intolerant'


class Client(db.Model):
    """Client model"""
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date)
    diet = db.Column(db.Enum(Diet), nullable=False)
    # medications = db.relationship('Medication', secondary='client_medications', back_populates='clients')
    start_date = db.Column(db.Date, nullable=False)
    # kin_id = db.relationship('User', secondary='clients_users', back_populates='kin_to')
    activities_attended = db.relationship('Activity', secondary='activities_clients', back_populates='clients_who_attended')
    # caregiver = db.relationship('User', secondary='clients_users', back_populates='clients_under_care')
    relation_to_user = db.Column(db.String(80))
    connected_to_user = db.relationship('User', secondary='clients_users', back_populates='connected_to_clients')

    def __repr__(self):
        return f"Client: '{self.first_name} {self.last_name}'"


class User(UserMixin, db.Model):
    """User model (client's family)"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80)) # had to get rid of nullable=False so that an instance of user
    # could be made at signup with only username and password, no other info needed
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    # kin_to = db.relationship('Client', secondary='clients_users', back_populates='kin_id')
    connected_to_clients = db.relationship('Client', secondary='clients_users', back_populates='connected_to_user')
    relation_to_clients = db.Column(db.String(80))
    # clients_under_care = db.relationship('Client', secondary='clients_users', back_populates='caregiver')
    role = db.Column(db.String(80))

    def __repr__(self):
        return f"User: '{self.first_name} {self.last_name}'"


class Activity(db.Model):
    """Activity model"""
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    clients_who_attended = db.relationship('Client', secondary='activities_clients', back_populates='activities_attended')

    def __repr__(self):
        return f"Activity: '{self.name}'"



client_user_table = db.Table('clients_users',
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

activity_client_table = db.Table('activities_clients',
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True)
)


class Message(db.Model):
    """Message model"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(100))
    sender = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Message: '{self.message}'"
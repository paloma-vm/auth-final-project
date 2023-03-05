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


# class Medication(db.Model):
#     """Medication model"""
#     __tablename__ = 'medications'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     dosage = db.Column(db.String(80), nullable=False)
#     frequency = db.Column(db.String(80), nullable=False)

#     def __repr__(self):
#         return f"Medication: '{self.name}"

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
    # start_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date) # trying to make it easier to test

    kin_id = db.relationship('User', secondary='clients_users', back_populates='clients')
    activities_attended = db.relationship('Activity', secondary='activities_clients', back_populates='clients_who_attended')
    caregiver = db.relationship('Caregiver', secondary='caregivers_clients', back_populates='clients_under_care')


    def __repr__(self):
        return f"Client: '{self.first_name} {self.last_name}'"

class Caregiver(db.Model):
    """Caregiver model"""
    __tablename__ = 'caregivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    clients_under_care = db.relationship('Client', secondary='caregivers_clients', back_populates='caregiver', lazy=True)

    def __repr__(self):
        return f"Caregiver: '{self.name}'"

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
    clients = db.relationship('Client', secondary='clients_users', back_populates='kin_id')
    relation_to_client = db.Column(db.String(80))

    def __repr__(self):
        return f"User: '{self.first_name} {self.last_name}'"

class Menu(db.Model):
    """Menu model"""
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    breakfast = db.Column(db.String(80), nullable=False)
    lunch = db.Column(db.String(80), nullable=False)
    dinner = db.Column(db.String(80), nullable=False)
    snacks = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Menu: '{self.date}'"

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

# client_medication_table = db.Table('client_medications',
#     db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True),
#     db.Column('medication_id', db.Integer, db.ForeignKey('medications.id'), primary_key=True)
# )

client_user_table = db.Table('clients_users',
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

activity_client_table = db.Table('activities_clients',
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True)
)

caregiver_client_table = db.Table('caregivers_clients',
    db.Column('caregiver_id', db.Integer, db.ForeignKey('caregivers.id'), primary_key=True),
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True)
)

class Message(db.Model):
    """Message model"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Message: '{self.message}'"
"""create db models to represent tables"""
from care_app.extensions import db
from sqlalchemy.orm import backref

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


class Medication(db.Model):
    """Medication model"""
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    dosage = db.Column(db.String(80), nullable=False)
    frequency = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Medication: '{self.name}"

class Client(db.Model):
    """Client model"""
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    diet = db.Column(db.Enum(Diet), nullable=False)
    medications = db.relationship('Medication', secondary='client_medications', backref='clients')
    move_in_date = db.Column(db.Date, nullable=False)
    kin = db.relationship('User', backref='user', lazy=True)
    activities_attended = db.relationship('Activity', secondary='client_activities', backref='clients')

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
    clients = db.relationship('Client', backref='caregiver', lazy=True)

    def __repr__(self):
        return f"Caregiver: '{self.name}'"

class User(db.Model):
    """User model (client's family)"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    clients = db.relationship('Client', backref='user', lazy=True)
    relation_to_client = db.Column(db.String(80), nullable=False)

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
    clients = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    def __repr__(self):
        return f"Activity: '{self.name}'"

client_medication_table = db.Table('client_medications',
    db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True),
    db.Column('medication_id', db.Integer, db.ForeignKey('medications.id'), primary_key=True)
)

class Message(db.Model):
    """Message model"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(80), nullable=False) #??
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Message: '{self.message}'"
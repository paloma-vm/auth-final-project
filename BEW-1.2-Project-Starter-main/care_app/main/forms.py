# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, IntegerField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from care_app.models import Diet, Client, User, Message

class ClientForm(FlaskForm):
    """Form to create a new client profile (resident profile)"""
    
    first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    last_name = StringField('Last Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    room_number = IntegerField('Room Number')
    date_of_birth = DateField('Date of Birth')
    diet = SelectField('Diet', choices=Diet.choices())
    # medications = QuerySelectMultipleField('Medications',
        # query_factory=lambda: Medication.query)
    # kin_id = StringField('Kin ID')
    start_date = DateField('Start Date')
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    """Form to create a new user profile (role=family or role=admin)"""
    first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    last_name = StringField('Last Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    email = StringField('Email',
        validators=[DataRequired(), Length(min=8, max=120, message="Your email must be between 8 and 120 characters long.")])
    # username = StringField('Username',
    #     validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=8, max=80, message="Your password must be between 8 and 80 characters long.")])
    connected_to_clients = QuerySelectMultipleField('Name of Client(s)',
        query_factory=lambda: Client.query)
    relation_to_clients = StringField('Relation to Client',
        validators=[DataRequired(), Length(min=2, max=80, message="Your relation must be between 8 and 80 characters long.")])
    role = StringField('Role: admin or user',
        validators=[DataRequired(), Length(min=2, max=80, message="Your relation must be either 'admin' or 'user'")])
    
    submit = SubmitField('Submit')

    def validate_email(self, email):
        """Check if email is already in use"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')


class MessageForm(FlaskForm):
    """Form to create a new message"""
    receiver = StringField('Email',
        validators=[DataRequired(), Length(min=8, max=120, message="The email address must be between 8 and 120 characters long.")])
    subject = StringField('Subject',
        validators=[DataRequired(), Length(min=2, max=80, message="Your subject must be between 2 and 80 characters long.")])
    body = TextAreaField('Body',
        validators=[DataRequired(), Length(min=2, max=1000, message="Your message must be between 2 and 1000 characters long.")])
    photo_url = StringField('Photo URL')
    submit = SubmitField('Submit')




# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from care_app.models import Diet

class ClientForm(FlaskForm):
    """Form to create a new client profile (resident profile)"""
    
    first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    last_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    room_number = IntegerField('Room Number')
    date_of_birth = DateField('Date of Birth',
        validators=[DataRequired])
    diet = SelectField('Diet', choices=Diet.choices())
    medications = QuerySelectMultipleField('Medications',
        query_factory=lambda: Medication.query)
    kin_id = StringField('Kin ID')
    move_in_date = DateField('Move-in Date')
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    """Form to create a new user profile (kin or family profile)"""
    first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    last_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    email = StringField('Email',
        validators=[DataRequired(), Length(min=8, max=120, message="Your email must be between 8 and 120 characters long.")])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=8, max=80, message="Your password must be between 8 and 80 characters long.")])
    clients = QuerySelectMultipleField('Name of Client(s)',
        query_factory=lambda: Client.query)
    relation_to_client = StringField('Relation to Client',
        validators=[DataRequired(), Length(min=2, max=80, message="Your relation must be between 8 and 80 characters long.")])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        """Check if email is already in use"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class CaregiverForm(FlaskForm):
    """Form to create a new caregiver profile"""
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2, max=80, message="Your name must be between 8 and 80 characters long.")])
    address = StringField('Address',
        validators=[DataRequired(), Length(min=2, max=80, message="Your address must be between 8 and 80 characters long.")])
    email = StringField('Email',
        validators=[DataRequired(), Length(min=8, max=120, message="Your email must be between 8 and 120 characters long.")])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=8, max=80, message="Your password must be between 8 and 80 characters long.")])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        """Check if email is already in use"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')



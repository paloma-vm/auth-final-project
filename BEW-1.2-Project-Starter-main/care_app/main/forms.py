# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
# from care_app.models import Audience, Book, Author, Genre, User

class ClientProfile(FlaskForm):
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
    family_id = StringField('Family ID')
    move_in_date = DateField('Move-in Date')
    submit = SubmitField('Submit')



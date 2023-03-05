from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime

from care_app.models import User, Client, Caregiver, Activity
from care_app.main.forms import ClientForm, UserForm, CaregiverForm, MessageForm

# Import app and db from care_app startup package so that we can run app
from care_app.extensions import app, db, bcrypt

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/') 
def homepage():
    
    return render_template('home.html')

@main.route('/create-client', methods=['GET', 'POST'])
@login_required
def create_client():
    '''Create a new Client'''
    form = ClientForm()
    # if form is submitted with no errors:
    if form.validate_on_submit():
        new_client = Client(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            room_number = form.room_number.data,
            date_of_birth = form.date_of_birth.data,
            diet = form.diet.data,
            start_date = form.start_date.data,
            )
        db.session.add(new_client)
        db.session.commit()

        flash('New client was created successfully.')
        return redirect(url_for('main.client_detail', client_id=new_client.id))

    return render_template('create-client.html', form=form)

@main.route('/client/<client_id>', methods=['GET', 'POST'])
@login_required
def client_detail(client_id):
    '''View and edit Client info'''
    client = Client.query.get(client_id)

    form = ClientForm(obj=client)
    # if form is submitted with no errors: update the Client object and save to the database
    # flash a confirmation message and redirect user to the client detail page
    if form.validate_on_submit():
        client.first_name = form.first_name.data
        client.last_name = form.last_name.data
        client.room_number = form.room_number.data
        client.date_of_birth = form.date_of_birth.data
        client.diet = form.diet.data
        # client.medications = form.medications.data
        client.start_date = form.start_date.data
        # client.kin_id = form.kin_id.data
    
        db.session.commit()

        flash('Client updated successfully.')
        return redirect(url_for('main.client_detail', client_id=client_id))
    
    # Send the form to the template and use it to render the form fields
    client = Client.query.get(client_id)
    return render_template('client-detail.html', client=client, form=form)

@main.route('/create-message', methods=['GET', 'POST'])
@login_required
def create_message():
    '''Create a new Message'''
    form = MessageForm()
    # if form is submitted with no errors:
    if form.validate_on_submit():
        new_message = Message(
            subject = form.subject.data,
            body = form.body.data,
            photo_url = form.photo_url.data
        )
        db.session.add(new_message)
        db.session.commit()

        flash('New message was created successfully.')
        return redirect(url_for('main.user_detail', message_id=new_message.id))

    return render_template('create-message.html', form=form)


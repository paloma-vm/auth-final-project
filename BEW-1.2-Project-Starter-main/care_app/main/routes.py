from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime

from care_app.models import User, Client, Activity, Message
from care_app.main.forms import ClientForm, UserForm, MessageForm

# Import app and db from care_app startup package so that we can run app
from care_app.extensions import app, db, bcrypt

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_clients = Client.query.all()
    return render_template('home.html', all_clients=all_clients)

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
    '''View Client info'''
    client = Client.query.get(client_id)

    return render_template('client-detail.html', client=client)
    # return redirect(url_for('main.client_detail', client=client))
    
@main.route('/edit-client/<client_id>', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    '''Edit Client info'''
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
    return render_template('edit-client.html', client=client, form=form)

@main.route('/create-message', methods=['GET', 'POST'])
@login_required
def create_message():
    '''Create a new Message'''
    form = MessageForm()
    # if form is submitted with no errors:
    if form.validate_on_submit():
        new_message = Message(
            receiver = form.receiver.data,
            subject = form.subject.data,
            body = form.body.data,
            photo_url = form.photo_url.data,
            sender_id = current_user.id,
            sender = User.query.get(current_user.id),
            timestamp = datetime.now().strftime('%A, %B %d, %Y, %H:%M')
            )
        db.session.add(new_message)
        db.session.commit()

        flash('New message was created successfully.')
        return redirect(url_for('main.message_detail', message_id=new_message.id))

    return render_template('create-message.html', form=form)

@main.route('/message/<message_id>', methods=['GET', 'POST'])
@login_required
def message_detail(message_id):
    '''View Message details'''
    message = Message.query.get(message_id)

    return render_template('message-detail.html', message=message)

@main.route('/edit-message/<message_id>', methods=['GET', 'POST'])
@login_required
def edit_message(message_id):
    '''Edit Message'''
    message = Message.query.get(message_id)

    form = MessageForm(obj=message)
    # if form is submitted with no errors: update the Message object and save to the database
    # flash a confirmation message and redirect user to the message detail page
    if form.validate_on_submit():
        message.receiver = form.receiver.data
        message.subject = form.subject.data
        message.body = form.body.data
        message.photo_url = form.photo_url.data
        message.sender_id = current_user.id
        message.sender = User.query.get(current_user.id)
        message.timestamp = datetime.now().strftime('%A, %B %d, %Y, %H:%M')
        
        db.session.commit()

        flash('Message updated successfully.')
        return redirect(url_for('main.message_detail', message_id=message_id))
    
    # Send the form to the template and use it to render the form fields
    message = Message.query.get(message_id)
    return render_template('edit-message.html',message=message, form=form)




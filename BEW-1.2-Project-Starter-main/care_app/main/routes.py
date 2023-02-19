from flask import Blueprint, render_template

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    return render_template('home.html')


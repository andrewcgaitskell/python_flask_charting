from flask import Blueprint, render_template

data_bp = Blueprint('data_bp', __name__)

# Define routes for the blueprint
@data_bp.route('/home')
def home():
    return render_template('static/home.html')

# Define routes for the blueprint
@data_bp.route('/help')
def dmtools_help():
    return render_template('static/dmtools_help.html')

@data_bp.route('/faq')
def dmtools_faq():
    return render_template('static/dmtools_faq.html')

@data_bp.route('/contact')
def dmtools_contact():
    return render_template('static/dmtools_contact.html')

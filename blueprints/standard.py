from flask import Blueprint, render_template

standard_bp = Blueprint('standard_bp', __name__)

# Define routes for the blueprint
@standard_bp.route('/home')
def home():
    return render_template('static/home.html')

# Define routes for the blueprint
@standard_bp.route('/help')
def dmtools_help():
    return render_template('static/dmtools_help.html')

@standard_bp.route('/faq')
def dmtools_faq():
    return render_template('static/dmtools_faq.html')

@standard_bp.route('/contact')
def dmtools_contact():
    return render_template('static/dmtools_contact.html')


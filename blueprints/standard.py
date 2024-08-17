from flask import Blueprint, render_template

standard_bp = Blueprint('main', __name__)

# Define routes for the blueprint
@standard_bp.route('/help')
def dmtools_help():
    return render_template('dmtools_help.html')

@standard_bp.route('/faq')
def dmtools_faq():
    return render_template('dmtools_faq.html')

@standard_bp.route('/contact')
def dmtools_contact():
    return render_template('dmtools_contact.html')

@standard_bp.route('/offcanvas')
def offcanvas():
    return render_template('offcanvas.html')

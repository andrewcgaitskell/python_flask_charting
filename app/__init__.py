"""Main application package."""
import os
from os import environ, path
from dotenv import load_dotenv

import secrets
import string
import random
# initializing size of string
N = 32

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

from flask import Flask, render_template, jsonify, send_file, send_from_directory, url_for

from flask_session import Session

import redis
from redis.exceptions import RedisError


from werkzeug.middleware.proxy_fix import ProxyFix

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

path = os.path.dirname(os.path.realpath(__file__))
from authlib.integrations.flask_client import OAuth

from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import DMToolsClient
from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import DMToolTestData
from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import PlotTrace

from brown_edu_dmtools.dmtools_jinja2_macros import env

import plotly.graph_objs as go
import json
import plotly

import matplotlib.pyplot as plt
import io

# for legend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

from blueprints.standard import standard_bp
from blueprints.charts import charts_bp
from blueprints.data import data_bp
from blueprints.viewing import viewing_bp
from blueprints.forms import forms_bp
from blueprints.tables import tables_bp

def init_app():
    app = Flask(__name__, static_folder='static')

    FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY") ## generated
    GOOGLE_CLIENT_ID_FLASK = environ.get("GOOGLE_CLIENT_ID_FLASK")
    GOOGLE_CLIENT_SECRET_FLASK = environ.get("GOOGLE_CLIENT_SECRET_FLASK")
    
    app.config['SESSION_COOKIE_PATH'] = '/'
  
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['GOOGLE_CLIENT_ID'] = GOOGLE_CLIENT_ID_FLASK
    app.config['GOOGLE_CLIENT_SECRET'] = GOOGLE_CLIENT_SECRET_FLASK
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT",'146585145368132386173505678016728509634')

    oauth = OAuth(app)
  
    with app.app_context(): 

        # Configure the session to use Redis
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_PERMANENT'] = False
        app.config['SESSION_USE_SIGNER'] = True
        app.config['SESSION_KEY_PREFIX'] = 'session:'
        app.config['SESSION_REDIS'] = redis.StrictRedis(host='container_redis_1', port=6379, db=0, decode_responses=False)
        
        Session(app)
        
        app.errorhandler(RedisError)
        def handle_redis_error(error):
            app.logger.error(f"Redis error encountered: {error}")
            return "A problem occurred with our Redis service. Please try again later.", 500
    
        app.register_blueprint(standard_bp, url_prefix="/")
        app.register_blueprint(charts_bp, url_prefix="/charts")
        app.register_blueprint(data_bp, url_prefix="/data")
        app.register_blueprint(viewing_bp, url_prefix="/viewing")
        app.register_blueprint(forms_bp, url_prefix="/forms")
        app.register_blueprint(tables_bp, url_prefix="/tables")
        
        # Define the navigation items
        def get_nav_items():
            return [
                {'text': 'Home', 'url': url_for('standard_bp.home')},
                {'text': 'Charts', 'url': url_for('charts_bp.charts')},
                {'text': 'Tables', 'url': url_for('tables_bp.tables')},
                {'text': 'Plotly', 'url': url_for('charts_bp.plotly')},
                {'text': 'Matplotlib', 'url': url_for('charts_bp.matplotlib')},
                {'text': 'Matplotlib Chart Legend', 'url': url_for('charts_bp.matplotlib_chart_legend')},
                {'text': 'Matplotlib Legend', 'url': url_for('charts_bp.matplotlib_legend')},
                {'text': 'Dynamic Form', 'url': url_for('forms_bp.dynamic_form')},
            ]
        
        # Context processor to make nav items available globally
        @app.context_processor
        def inject_nav_items():
            return dict(nav_items=get_nav_items())

        return app

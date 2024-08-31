from flask import session
from app import init_app
import pickle
application = init_app()

from urllib.parse import urlparse, urlunparse, quote

import msgpack

from secure_cookie.session import SessionMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Request, Response, ResponseStream
from werkzeug.debug import DebuggedApplication
from werkzeug.utils import redirect

from jinja2 import Environment, FileSystemLoader, PackageLoader

from pprint import pformat
from time import time

import redis
import requests
import chardet

import json
import ast
import chardet
from datetime import datetime

import requests

import io

import os
import sys
from os import environ, path
from dotenv import load_dotenv

import json

fastapi_url = environ.get("FASTAPI_URL")

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, "/app/.env"))

print('BASE_DIR')
print(BASE_DIR)

app = init_app()

class Middleware:

    def __init__(self, wsgi):
        self.wsgi = wsgi
        try:
            self.redisserver = redis.StrictRedis(host='container_redis_1', port=6379,db=0, decode_responses=False)
            self.redisserver.ping()  # Test the connection
            print("Connected to Redis")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
        
        self.SESSION_COOKIE_NAME = "session"
        self.template_path = path.join(BASE_DIR, "/workdir/flask_application/app/templates")
        self.jinja_env = Environment(loader=FileSystemLoader(self.template_path),
                             autoescape=True)
       
        
    
    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        #t = self.env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')
    
    def __call__(self, environ, start_response):
        
        request = Request(environ)
        ## -------------------------------------------------
        ## the following simplifies retrieving session data
        ## google did not find this solution
        ## I used chatgpt to guide me towards the request context
        ## -------------------------------------------------
        with app.request_context(environ):
            # Check for session data or specific conditions
            # all_session = session.get('*')
            path = environ.get('PATH_INFO', '')

            #print('wsgi - app_context')
            #print('all_session>>>>>>', session)
            #print('environ >>>>>>', environ)
            #dmtool_userid = session['dmtool_userid']
            try:
                dmtool_authorised = session['dmtool_authorised']
            except:
                dmtool_authorised = 0
            #print('dmtool_userid >>>>>>', dmtool_userid)
            #print('dmtool_authorised >>>>>>', dmtool_authorised)
            # Protect specific routes
            unauthorised_response = self.render_template('application_unauthorized_local.html')
            
            if ('data' not in path and 'plot' not in path and 'baseapp' not in path ) :
                #print('wsgi and session_app and baseapp not in path')
                return self.wsgi(environ,start_response)
                #return unauthorised_response(environ, start_response)
            elif ('data' in path or 'baseapp' in path or 'plot' in path) and (dmtool_authorised==1) :
                return self.wsgi(environ,start_response)
                #return unauthorised_response(environ, start_response)
            else:
                unauthorised_response = self.render_template('application_unauthorized_local.html')
                return unauthorised_response(environ, start_response)
            #return self.wsgi(environ,start_response)
            
            # Call the next middleware or the main Flask app
            return self.app(environ, start_response)

        
application = Middleware(application)

application = DebuggedApplication(application, True)

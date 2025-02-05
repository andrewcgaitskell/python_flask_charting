## get api key and user id from local .env file
from dotenv import load_dotenv
import os
from os import environ, path

import pandas as pd

import json

import datetime

BASE_DIR = os.getcwd()

print("BASE_DIR >>>>>>>>>>>>>>", BASE_DIR)

load_dotenv(path.join(BASE_DIR, ".env"))
MY_DMTOOLS_APIKEY = environ.get("MY_DMTOOLS_APIKEY")
MY_DMTOOLS_USERID = environ.get("MY_DMTOOLS_USERID")

from flask import Blueprint

from flask import Flask, render_template, jsonify, send_file, send_from_directory, request, redirect, url_for

import requests

from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import DMToolsClient
from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import DMToolTestData
from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import PlotTrace

from brown_edu_dmtools.dmtools_jinja2_macros import env

Client = DMToolsClient(MY_DMTOOLS_USERID, MY_DMTOOLS_APIKEY)

forms_bp = Blueprint('forms_bp', __name__)

# Generate form data from the model schema
def generate_form_data_from_schema(subject_in, data_in):
    data = data_in[0]
    form_data = {}
    schema = Client.schema(subject=subject_in)
    print(schema)
    properties = schema.get("properties", {})

    for field_name, field_info in properties.items():
        print("field_info >>>>>" , field_info)
      
        field_label = field_info.get("title", field_name.capitalize())
        field_type = field_info['anyOf'][0]['type']
        try:        
            field_format = field_info['anyOf'][0]['format']
        except:
            field_format = 'text'
        
        # Determine the input type based on the Pydantic field type
        
        if field_type == "integer":
            input_type = "number"
        elif field_type == "float":
            input_type = "number"
        elif field_type == "bool":
            input_type = "checkbox"
        elif field_format == "date-time":
            input_type = "datetime-local"
        # Add more type mappings as needed

        else:
            input_type = "text"  # Fallback to text for unknown types

        print("field_type>>>>" , field_type, " field_format >>", field_format,"  label>>>>",  field_label,"  input type>>>>>", input_type)

        try:
            form_data[field_name] = {
                "label": field_label,
                "type": input_type,
                "value": data[field_name]
            }
        except:
            form_data[field_name] = {
                "label": field_label,
                "type": input_type,
                "value": ""
            }

    
    return form_data

@forms_bp.route('/edit/<subject_in>/<id_in>', methods=['GET', 'POST'])
def edit_model(subject_in,id_in):
    schema = Client.schema(subject=subject_in)
    data = Client.read(subject=subject_in, id=id_in)
    if not schema:
        return "Model not found", 404

    if request.method == 'POST':
        # Handle form submission here
        data = request.form.to_dict()
        # You can validate this data or send it back to the FastAPI server
        return "Form submitted successfully!"

    form_data = generate_form_data_from_schema(subject_in, data)
    return render_template('forms/schema_form.html', form_data=form_data, action=f'/edit/{subject_in}/{id_in}')


@forms_bp.route('/dynamic_form')
def dynamic_form():
    fields = [
        {'id': 'name', 'label': 'Name', 'type': 'text', 'name': 'name'},
        {'id': 'email', 'label': 'Email', 'type': 'email', 'name': 'email'},
        {'id': 'age', 'label': 'Age', 'type': 'number', 'name': 'age'}
    ]
    #template = env.get_template('forms/dynamic_form.html')
    #return template.render(fields=fields)
    return render_template('forms/dynamic_form.html', fields=fields)


@forms_bp.route('/<subject>/create/', methods=['GET', 'POST'])
def create_item(subject):
    if request.method == 'POST':
        # Submit form data to FastAPI
        form_dict = request.form.to_dict()
        print("form_dict>>>>>>>>>>>>>>>>>>>>", form_dict)
        form_dict.pop('id', None)
        form_dict.pop('created_at', None)
        form_dict.pop('modified_at', None)
        form_dict.pop('archived_at', None)
        Client.create(subject=subject,data=form_dict)
        return redirect(url_for('forms_bp.list_items', subject=subject))
    
    # Fetch the model schema to dynamically generate the form
    empty_schema = Client.read(subject=subject,id=-1)
    form_data = generate_form_data_from_schema(subject, empty_schema)
    
    return render_template('forms/schema_form.html', form_data=form_data)

@forms_bp.route('/<subject>/update/<item_id>/', methods=['GET', 'POST'])
def update_item(subject, item_id):
    if request.method == 'POST':
        form_data = request.form.to_dict()
        Client.update(id=item_id, data=form_data)
        return redirect(url_for('forms_bp.list_items', subject=subject))
    
    item = Client.read(subject=subject,id=item_id)
    
    form_data = generate_form_data_from_schema(subject, item)
    
    return render_template('forms/schema_form.html', form_data=form_data)

@forms_bp.route('/<subject>/delete/<item_id>/')
def delete_item(subject, item_id):
    Client.delete(id=item_id,subject=subject)
    return redirect(url_for('forms_bp.list_items', subject=subject))

## get api key and user id from local .env file
from dotenv import load_dotenv
import os
from os import environ, path

import datetime

BASE_DIR = os.getcwd()

print("BASE_DIR >>>>>>>>>>>>>>", BASE_DIR)

load_dotenv(path.join(BASE_DIR, ".env"))
MY_DMTOOLS_APIKEY = environ.get("MY_DMTOOLS_APIKEY")
MY_DMTOOLS_USERID = environ.get("MY_DMTOOLS_USERID")

from flask import Blueprint

from flask import Flask, render_template, jsonify, send_file, send_from_directory, request

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

@forms_bp.route('/list_subjects')
def list():
    # List available models and their items
    subjects = ["data", "data_display", "ownership", "plot", "experiment", "limit_display"]
    return render_template('list_subjects.html', subjects=subjects)

@app.route('/list_items/<subject>/')
def list_items(subject):
    # Fetch list of items for the model from FastAPI
    items = Client.read(subject=subject)
    return render_template('list_items.html', subject=subject, items=items)

@app.route('/<subject>/create/', methods=['GET', 'POST'])
def create_item(subject):
    if request.method == 'POST':
        # Submit form data to FastAPI
        form_data = request.form.to_dict()
        Client.create(data=form_data)
        return redirect(url_for('list_items', subject=subject))
    
    # Fetch the model schema to dynamically generate the form
    schema = Client.schema(subject=subject_in)
    empty_schema = schema()
    form_data = generate_form_data_from_schema(subject_in, empty_schema)
    
    return render_template('forms/schema_form.html', form_data=form_data)

@app.route('/<subject>/update/<item_id>/', methods=['GET', 'POST'])
def update_item(subject, item_id):
    if request.method == 'POST':
        form_data = request.form.to_dict()
        Client.update(id=item_id, data=form_data)
        return redirect(url_for('list_items', subject=subject))
    
    item = Client.read(subject=subject,id=item_id)
    schema = Client.schema(subject=subject)
    form_data = generate_form_data_from_schema(subject_in, item)
    
    return render_template('forms/schema_form.html', form_data=form_data)

@app.route('/<subject>/delete/<item_id>/')
def delete_item(subject, item_id):
    Client.delete(id=item_id,subject=subject)
    return redirect(url_for('list_items', subject=subject))

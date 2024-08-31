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

tables_bp = Blueprint('tables_bp', __name__)

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


@tables_bp.route('/list')
def tables():
    # List available models and their items
    subjects = ["data", "data_display", "ownership", "plot", "dropdown","graph", "limit_display"]
    return render_template('tables/list_subjects.html', subjects=subjects)

@tables_bp.route('/static_crud_table')
def crud_table():
    return render_template('tables/crud_table.html')

@tables_bp.route('/<subject_in>/dynamic_view')
def dynamic_crud_table(subject_in):
    params = {
    'value': '1',
    'key_subject': subject_in,
    'key_purpose': 'list_table'
    }

    params_as_string = json.dumps(params)

    # Pass the encoded query to the API client
    r = Client.query(subject='graph', query_criteria=params_as_string)

    new_df = pd.DataFrame(data=r)
    table_columns = new_df['key'].tolist()
    columns = []
    for tc in table_columns:
        append_dict = {'key': tc, 'label': tc}
        columns.append(append_dict)

    print(columns)
    
    # generate_form_data_from_schema(subject_in, data_in)
    
    # Define the columns and data
    '''
    columns = [
        {'key': 'id', 'label': 'ID'},
        {'key': 'name', 'label': 'Name'},
        {'key': 'age', 'label': 'Age'},
        {'key': 'email', 'label': 'Email'}
    ]
    '''
    '''
    data = [
        {'id': 1, 'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'age': 25, 'email': 'jane@example.com'}
    ]
    '''
    r = Client.read(subject=subject_in)

    print(r)

    # Specify the keys you want to select
    keys_to_select = table_columns
    
    # Iterate over the list of dictionaries and select only the specified keys
    data = [{key: item[key] for key in keys_to_select} for item in r]

    # Pass the columns and data to the template
    return render_template('tables/dynamic_view.html', columns=columns, data=data)

@tables_bp.route('/list_items/<subject>/')
def list_items(subject):
    # Fetch list of items for the model from FastAPI
    items = Client.read(subject=subject)
    return render_template('tables/list_items.html', subject=subject, items=items)


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
        
        form_data[field_name] = {
            "label": field_label,
            "type": input_type,
            "value": data[field_name]
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

if __name__ == '__main__':
    app.run(debug=True)

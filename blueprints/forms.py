## get api key and user id from local .env file
from dotenv import load_dotenv
import os
from os import environ, path

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
def generate_form_data_from_schema(subject_in):
    form_data = {}
    schema = Client.schema(subject=subject_in)
    properties = schema.get("properties", {})
    for field_name, field in properties.items():
        form_data[field_name] = {
            "label": field.get("title", field_name.capitalize()),
            "type": "text" if field.get("type") == "string" else "number",
            "value": ""
        }
    return form_data

@forms_bp.route('/edit/<subject_in>', methods=['GET', 'POST'])
def edit_model(subject_in):
    schema = Client.schema(subject=subject_in)
    if not schema:
        return "Model not found", 404

    if request.method == 'POST':
        # Handle form submission here
        data = request.form.to_dict()
        # You can validate this data or send it back to the FastAPI server
        return "Form submitted successfully!"

    form_data = generate_form_data_from_schema(subject_in)
    return render_template('forms/pydantic_form.html', form_data=form_data, action=f'/edit/{model_name}')

if __name__ == '__main__':
    app.run(debug=True)

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

from flask import Flask, render_template, jsonify, send_file, send_from_directory

from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import DMToolsClient
from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import DMToolTestData
from brown_edu_dmtools.dmtools_client_package.dmtools_client_module import PlotTrace

from brown_edu_dmtools.dmtools_jinja2_macros import env

Client = DMToolsClient(MY_DMTOOLS_USERID, MY_DMTOOLS_APIKEY)

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

viewing_bp = Blueprint('viewing_bp', __name__)

# Example data for the table
data = [
    {"id": 1, "name": "Item 1", "value": 10},
    {"id": 2, "name": "Item 2", "value": 20},
    {"id": 3, "name": "Item 3", "value": 30},
]

form_metadata = [
{'field:'date_of_announcement','label:'Date of Announcement','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'archived_at','label:'Archived At','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'created_at','label:'Created At','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'date_of_run_end','label:'Date of Run End','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'date_of_run_start','label:'Date of Run Start','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'date_official','label:'Date Official','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'updated_at','label:'Updated At','type':'datetime','default_value':'1980-01-01 00:00:00'},
{'field:'class_id','label:'Class ID','type':'int','default_value':'-1'},
{'field:'creator_id','label:'Creator ID','type':'int','default_value':'-1'},
{'field:'data_id','label:'Data ID','type':'int','default_value':'-1'},
{'field:'greatest_hit','label:'Greatest Hit','type':'int','default_value':'-1'},
{'field:'id','label:'ID','type':'int','default_value':'-1'},
{'field:'limit_id','label:'Limit ID','type':'int','default_value':'-1'},
{'field:'no_id','label:'No ID','type':'int','default_value':'-1'},
{'field:'official','label:'Official','type':'int','default_value':'-1'},
{'field:'old_id','label:'Old ID','type':'int','default_value':'-1'},
{'field:'old_plot_id','label:'Old Plot ID','type':'int','default_value':'-1'},
{'field:'old_user_id','label:'Old User ID','type':'int','default_value':'-1'},
{'field:'open','label:'Open','type':'int','default_value':'-1'},
{'field:'plot_id','label:'Plot ID','type':'int','default_value':'-1'},
{'field:'public','label:'Public','type':'int','default_value':'-1'},
{'field:'rating','label:'Rating','type':'int','default_value':'-1'},
{'field:'user_id','label:'User ID','type':'int','default_value':'-1'},
{'field:'x_max','label:'X Max','type':'int','default_value':'-1'},
{'field:'x_min','label:'X Min','type':'int','default_value':'-1'},
{'field:'y_max','label:'Y Max','type':'int','default_value':'-1'},
{'field:'y_min','label:'Y Min','type':'int','default_value':'-1'},
{'field:'year','label:'Year','type':'int','default_value':'-1'},
{'field:'class_name','label:'Class Name','type':'text','default_value':'class_name'},
{'field:'color','label:'Color','type':'text','default_value':'color'},
{'field:'data_label','label:'Data Label','type':'text','default_value':'data_label'},
{'field:'data_reference','label:'Data Reference','type':'text','default_value':'data_reference'},
{'field:'default_color','label:'Default Color','type':'text','default_value':'default_color'},
{'field:'default_style','label:'Default Style','type':'text','default_value':'default_style'},
{'field:'experiment','label:'Experiment','type':'text','default_value':'experiment'},
{'field:'file_name','label:'File Name','type':'text','default_value':'file_name'},
{'field:'measurement_type','label:'Measurement Type','type':'text','default_value':'measurement_type'},
{'field:'name','label:'Name','type':'text','default_value':'name'},
{'field:'nomhash','label:'Nomhash','type':'text','default_value':'nomhash'},
{'field:'old_name','label:'Old Name','type':'text','default_value':'old_name'},
{'field:'result_type','label:'Result Type','type':'text','default_value':'result_type'},
{'field:'spin_dependency','label:'Spin Dependency','type':'text','default_value':'spin_dependency'},
{'field:'style','label:'Style','type':'text','default_value':'style'},
{'field:'subject','label:'Subject','type':'text','default_value':'subject'},
{'field:'x_rescale','label:'X Rescale','type':'text','default_value':'x_rescale'},
{'field:'x_units','label:'X Units','type':'text','default_value':'x_units'},
{'field:'y_rescale','label:'Y Rescale','type':'text','default_value':'y_rescale'},
{'field:'y_units','label:'Y Units','type':'text','default_value':'y_units'},
{'field:'data','label:'Data','type':'textarea','default_value':'data'},
{'field:'data_comment','label:'Data Comment','type':'textarea','default_value':'data_comment'},
{'field:'data_values','label:'Data Values','type':'textarea','default_value':'data_values'},
{'field:'legend_eps','label:'Legend EPS','type':'textarea','default_value':'legend_eps'},
{'field:'legend_png','label:'Legend PNG','type':'textarea','default_value':'legend_png'},
{'field:'plot_eps','label:'Plot EPS','type':'textarea','default_value':'plot_eps'},
{'field:'plot_png','label:'Plot PNG','type':'textarea','default_value':'plot_png'}
]


@viewing_bp.route('/selection_table')
def selection_table():
    # Render a template with a table of items
    return render_template('tables/selection_table.html', data=data)

@viewing_bp.route('/selected_chart/<int:item_id>')
def selected_chart(item_id):
    # Find the selected item by ID
    selected_item = next((item for item in data if item['id'] == item_id), None)
    
    if not selected_item:
        return "Item not found", 404
    
    # Pass the selected item's data to the chart template
    return render_template('tables/selected_chart.html', item=selected_item)

@viewing_bp.route('/view_details/<string:subject_in>/<int:item_id>')
def view_details(subject_in, item_id):
    
    subject_data = Client.read(subject=subject_in, id=item_id)
    
    form_data = subject_data[0]
    
    if not subject_data:
        return "Item not found", 404
    
    dropdown_options = {
    "name": ["A", "B", "C"]
    }
    
    # Pass the selected item's data to the chart template
    return render_template('tables/view_details.html', data=form_data, dropdown_options=dropdown_options)


@viewing_bp.route('/charts')
def view_chart():
    chart_data = {
        'title': 'Sample Line Chart',
        'xLabel': 'Time (s)',
        'yLabel': 'Value (V)',
        'data': {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            'datasets': [{
                'label': 'My First dataset',
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'data': [65, 59, 80, 81, 56, 55, 40]
            }]
        }
    }
    #template = env.get_template('charts/chart.html')
    #return template.render(chart_data=chart_data)
    return render_template('charts/chart.html', chart_data=chart_data)

'''
# Example list of dictionaries
dynamic_data = [
    {"id": 1, "name": "Alice", "age": 30, "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "age": 25, "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "age": 35, "email": "charlie@example.com"}
]

keys = dynamic_data[0].keys()

column_size_json = {}

for k in keys:
    column_size_json[k] = 0
    
for dd in dynamic_data:
    for attribute, value in dd.items():
        if column_size_json[attribute] < len(str(value)):
            column_size_json[attribute] =  len(str(value))

print(column_size_json)
'''

## optimised!

def get_column_sizes(dynamic_data_in):
    # Initialize dictionary to store maximum length of each column
    column_size_json = {}
    
    # Iterate through each dictionary in the list
    for item in dynamic_data_in:
        for key, value in item.items():
            # Update the maximum length for each key
            column_size_json[key] = max(column_size_json.get(key, 0), len(str(value)))
    
    return column_size_json

@viewing_bp.route('/dynamic_table')
def dynamic_table():
    # Calculate maximum width for each column
    
    column_widths_in_characters = get_column_sizes(dynamic_data)
    
    # Calculate the total width
    total_width = sum(column_widths_in_characters.values())
    
    # Calculate column widths as percentages
    column_widths_as_percentage = {col: (width / total_width) * 100 for col, width in column_widths_in_characters.items()}
    
    print(column_widths_as_percentage)
    
    return render_template('tables/dynamic_widths.html', data=dynamic_data, column_widths=column_widths_as_percentage)

@viewing_bp.route('/all_subject_data/<string:subject_in>')
def dynamic_subject(subject_in):
    # Calculate maximum width for each column
    subject_data = Client.read(subject=subject_in)

    # Keys to keep
    if subject_in == 'plot':
        keys_to_keep = ['id', 'subject', 'name']
        # Create a new list of dictionaries with only the selected keys
        filtered_data = [{key: item[key] for key in keys_to_keep} for item in subject_data]
    elif subject_in == 'data':
        keys_to_keep = ['id',  'subject','data_reference']
        # Create a new list of dictionaries with only the selected keys
        filtered_data = [{key: item[key] for key in keys_to_keep} for item in subject_data]
    else:
        try:
            keys_to_keep = ['id', 'subject', 'name']
            # Create a new list of dictionaries with only the selected keys
            filtered_data = [{key: item[key] for key in keys_to_keep} for item in subject_data]
        except:
            filtered_data = subject_data

    column_widths_in_characters = get_column_sizes(filtered_data)
    
    # Calculate the total width
    total_width = sum(column_widths_in_characters.values())
    
    # Calculate column widths as percentages
    column_widths_as_percentage = {col: (width / total_width) * 100 for col, width in column_widths_in_characters.items()}
    
    print(column_widths_as_percentage)
    
    return render_template('tables/dynamic_widths.html', data=subject_data, column_widths=column_widths_as_percentage)


@viewing_bp.route('/dynamic_form')
def dynamic_form():
    form_data = [
        {"name": "first_name", "label": "First Name", "type": "text", "required": True},
        {"name": "last_name", "label": "Last Name", "type": "text", "required": True},
        {"name": "email", "label": "Email", "type": "email", "required": True},
        {"name": "password", "label": "Password", "type": "password", "required": True},
        {"name": "gender", "label": "Gender", "type": "select", "options": ["Male", "Female", "Other"]},
        {"name": "bio", "label": "Bio", "type": "textarea"}
    ]
    return render_template('tables/dynamic_form.html', form_data=form_data)

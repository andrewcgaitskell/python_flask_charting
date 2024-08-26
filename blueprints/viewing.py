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

## optimised!

def get_column_sizes(dynamic_data_in):
    # Initialize dictionary to store maximum length of each column
    column_size_json = {}
    
    # Iterate through each dictionary in the list
    for item in dynamic_data:
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

@viewing_bp.route('/all_subject_data/<str:subject_in>})
def dynamic_subject():
    # Calculate maximum width for each column
    subject_data = Client.read(subject=subject_in)
    
    column_widths_in_characters = get_column_sizes(subject_data)
    
    # Calculate the total width
    total_width = sum(column_widths_in_characters.values())
    
    # Calculate column widths as percentages
    column_widths_as_percentage = {col: (width / total_width) * 100 for col, width in column_widths_in_characters.items()}
    
    print(column_widths_as_percentage)
    
    return render_template('tables/dynamic_widths.html', data=dynamic_data, column_widths=column_widths_as_percentage)

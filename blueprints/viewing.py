from flask import Blueprint

from flask import Flask, render_template, jsonify, send_file, send_from_directory

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
    return render_template('table/selection_table.html', data=data)

@viewing_bp.route('/selected_chart/<int:item_id>')
def selected_chart(item_id):
    # Find the selected item by ID
    selected_item = next((item for item in data if item['id'] == item_id), None)
    
    if not selected_item:
        return "Item not found", 404
    
    # Pass the selected item's data to the chart template
    return render_template('table/selected_chart.html', item=selected_item)


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


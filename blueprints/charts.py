from flask import Blueprint

from flask import Flask, render_template, jsonify, send_file, send_from_directory

from flask import request

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

import base64

## get api key and user id from local .env file
from dotenv import load_dotenv
import os
from os import environ, path
#BASE_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = os.getcwd()
#load_dotenv(path.join(BASE_DIR, ".env"))
load_dotenv(path.join(BASE_DIR, ".env"), override=True)
MY_DMTOOLS_APIKEY = environ.get("MY_DMTOOLS_APIKEY")
MY_DMTOOLS_USERID = environ.get("MY_DMTOOLS_USERID")
Client = DMToolsClient(MY_DMTOOLS_USERID, MY_DMTOOLS_APIKEY)
#Client.request_header

local_data = {
    'screenHeight': '600px',
    'screenWidth': '600px'
}


charts_bp = Blueprint('charts_bp', __name__)

@charts_bp.route('/charts')
def charts():
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




@charts_bp.route('/plotly')
def plotly():
    # Create a simple interactive Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='lines+markers', name='Line Plot'))

    # Convert the Plotly figure to JSON
    graph_json = fig.to_json()

    #template = env.get_template('plotly.html')
    #return template.render(graph_json=graph_json)
    return render_template('charts/plotly.html', graph_json=graph_json)

@charts_bp.route('/matplotlib')
def matplotlib():
    #template = env.get_template('charts/matplotlib.html')
    #return template.render()
    return render_template('charts/matplotlib.html')


@charts_bp.route('/css_variable/')
def index():
    return render_template('charts/css_variable.html')

@charts_bp.route('/receive_css_variable', methods=['POST'])
def receive_css_variable():
    data = request.get_json()
    main_color = data.get('mainColor')
    screen_height = data.get('screenHeight')
    screen_width = data.get('screenWidth')
    local_data['screenHeight'] = screen_height
    local_data['screenWidth'] = screen_width
    
    # Process the CSS variable value if needed
    print(f"Received CSS variable - Main Color: {main_color}")
    print(f"Received CSS variable - Screen Height : {local_data['screenHeight']}")
    print(f"Received CSS variable - Screen Width: {local_data['screenWidth']}")

    # Respond with a JSON object
    return jsonify({'status': 'success', 'mainColor': main_color,'screenHeight' : screen_height,'screenWidth' : screen_width  })


@charts_bp.route('/chart_frame/<plot_id_in>')
def chart_frame(plot_id_in):
    
    dmtools_plot = Client.get_mpl_plot(plot_id_in, width_in=400, height_in=400)
    
    # Save it to a BytesIO object
    img = io.BytesIO()
    dmtools_plot.savefig(img, format='png')
    img.seek(0)
    dmtools_plot.clf()  # Clear the current figure
    # Encode to base64
    dmtools_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    dmtools_legend = Client.get_mpl_legend(plot_id_in, width_in=600, height_in=200)
    # Save it to a BytesIO object
    img = io.BytesIO()
    dmtools_legend.savefig(img, format='png')
    img.seek(0)
    dmtools_legend.clf()  # Clear the current figure
    # Encode to base64
    dmtools_legend_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return render_template('charts/chart_frame.html',plot=dmtools_plot_url, legend=dmtools_legend_url)

@charts_bp.route('/matplotlib_png.png')
def matplotlib_png():
    # Generate a Matplotlib figure
    fig, ax = plt.subplots()
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]
    ax.plot(x, y)
    ax.set(title='Sample Line Chart', xlabel='X-axis', ylabel='Y-axis')

    # Save it to a BytesIO object
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)

    return send_file(output, mimetype='image/png')

@charts_bp.route('/matplotlib_chart_legend')
def matplotlib_chart_legend():
    #template = env.get_template('charts/matplotlib_chart_legend.html')
    #return template.render()
    return render_template('charts/matplotlib_chart_legend.html')

@charts_bp.route('/matplotlib_chart_legend_png.png')
def matplotlib_chart_legend_png():
    # Sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Create the plot
    fig, ax = plt.subplots()
    
    # Plot lines
    line1, = ax.plot(x, y1, color='blue', label='Sine Wave')
    line2, = ax.plot(x, y2, color='green', label='Cosine Wave')
    
    # Plot filled areas with patterns
    ax.fill_between(x, y1, color='blue', alpha=0.3, hatch='/', label='Sine Fill')
    ax.fill_between(x, y2, color='green', alpha=0.3, hatch='\\', label='Cosine Fill')
    
    # Create custom legend handles
    line1_handle = mlines.Line2D([], [], color='blue', label='Sine Wave', linestyle='-')
    line2_handle = mlines.Line2D([], [], color='green', label='Cosine Wave', linestyle='-')
    
    fill1_handle = mpatches.Patch(color='blue', alpha=0.3, hatch='/', label='Sine Fill')
    fill2_handle = mpatches.Patch(color='green', alpha=0.3, hatch='\\', label='Cosine Fill')
    
    # Combine handles
    handles = [line1_handle, line2_handle, fill1_handle, fill2_handle]
    labels = [handle.get_label() for handle in handles]
    
    # Create legend
    ax.legend(handles=handles, labels=labels, loc='upper right')
    
    # Save it to a BytesIO object
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    
    return send_file(output,  mimetype='image/png')

@charts_bp.route('/matplotlib_legend')
def matplotlib_legend():
    #template = env.get_template('charts/matplotlib_legend.html')
    #return template.render()
    return render_template('charts/matplotlib_legend.html')

@charts_bp.route('/matplotlib_legend_png.png')
def matplotlib_legend_png():
    # Create custom legend handles
    line1_handle = mlines.Line2D([], [], color='blue', label='Sine Wave', linestyle='-')
    line2_handle = mlines.Line2D([], [], color='green', label='Cosine Wave', linestyle='-')
    
    fill1_handle = mpatches.Patch(color='blue', alpha=0.3, hatch='/', label='Sine Fill')
    fill2_handle = mpatches.Patch(color='green', alpha=0.3, hatch='\\', label='Cosine Fill')
    
    # Combine handles and labels
    handles = [line1_handle, line2_handle, fill1_handle, fill2_handle]
    labels = [handle.get_label() for handle in handles]
    
    # Create a new figure just for the legend
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.legend(handles=handles, labels=labels, loc='center')
    ax.axis('off')  # Hide the axes
    
    # Save it to a BytesIO object
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    
    return send_file(output,  mimetype='image/png')




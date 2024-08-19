from flask import Flask, render_template, jsonify, send_file, send_from_directory

from dmtools_jinja2_macros import env

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

from blueprints.standard import standard_bp

app = Flask(__name__, static_folder='static')

app.register_blueprint(standard_bp)

@app.route('/')
def home():
    return render_template('base.html')


@app.route('/charts')
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
    return render_template('chart.html', chart_data=chart_data)

@app.route('/tables')
def tables():
    table_data = [
        {'column1': 'A1', 'column2': 'B1', 'column3': 'C1'},
        {'column1': 'A2', 'column2': 'B2', 'column3': 'C2'},
        {'column1': 'A3', 'column2': 'B3', 'column3': 'C3'}
    ]
    #return render_template('table.html', table_data=table_data)
    template = env.get_template('table.html')
    return template.render(table_data=table_data)


@app.route('/plotly')
def plotly():
    # Create a simple interactive Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='lines+markers', name='Line Plot'))

    # Convert the Plotly figure to JSON
    graph_json = fig.to_json()
    
    return render_template('plotly.html', graph_json=graph_json)

@app.route('/matplotlib')
def matplotlib():
    return render_template('matplotlib.html')

@app.route('/matplotlib_png.png')
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

@app.route('/matplotlib_chart_legend')
def matplotlib_chart_legend():
    return render_template('matplotlib_chart_legend.html')

@app.route('/matplotlib_chart_legend_png.png')
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

@app.route('/matplotlib_legend')
def matplotlib_legend():
    return render_template('matplotlib_legend.html')

@app.route('/matplotlib_legend_png.png')
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

@app.route('/dynamic_form')
def dynamic_form():
    fields = [
        {'id': 'name', 'label': 'Name', 'type': 'text', 'name': 'name'},
        {'id': 'email', 'label': 'Email', 'type': 'email', 'name': 'email'},
        {'id': 'age', 'label': 'Age', 'type': 'number', 'name': 'age'}
    ]
    return render_template('dynamic_form.html', fields=fields)
                       
if __name__ == '__main__':
    app.run(debug=True)

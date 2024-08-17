from flask import Flask, render_template, jsonify

import plotly.graph_objs as go
import json
import plotly

app = Flask(__name__)

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
    return render_template('table.html', table_data=table_data)

@app.route('/plotly')
def index():
    # Create a simple interactive Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='lines+markers', name='Line Plot'))

    # Convert the Plotly figure to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('plotly.html', graph_json=graph_json)

if __name__ == '__main__':
    app.run(debug=True)

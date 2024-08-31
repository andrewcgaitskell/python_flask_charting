from flask import Flask, render_template, jsonify, send_file, send_from_directory, url_for

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

from blueprints.standard import standard_bp
from blueprints.charts import charts_bp
from blueprints.data import data_bp
from blueprints.viewing import viewing_bp
from blueprints.forms import forms_bp

app = Flask(__name__, static_folder='static')

app.register_blueprint(standard_bp, url_prefix="/")
app.register_blueprint(charts_bp, url_prefix="/charts")
app.register_blueprint(data_bp, url_prefix="/data")
app.register_blueprint(viewing_bp, url_prefix="/viewing")
app.register_blueprint(forms_bp, url_prefix="/forms")

# Define the navigation items
def get_nav_items():
    return [
        {'text': 'Home', 'url': url_for('standard_bp.home')},
        {'text': 'Charts', 'url': url_for('charts_bp.charts')},
        {'text': 'Tables', 'url': url_for('table_bp.tables')},
        {'text': 'Plotly', 'url': url_for('charts_bp.plotly')},
        {'text': 'Matplotlib', 'url': url_for('charts_bp.matplotlib')},
        {'text': 'Matplotlib Chart Legend', 'url': url_for('charts_bp.matplotlib_chart_legend')},
        {'text': 'Matplotlib Legend', 'url': url_for('charts_bp.matplotlib_legend')},
        {'text': 'Dynamic Form', 'url': url_for('forms_bp.dynamic_form')},
    ]

# Context processor to make nav items available globally
@app.context_processor
def inject_nav_items():
    return dict(nav_items=get_nav_items())

                       
if __name__ == '__main__':
    app.run(debug=True)

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

from blueprints.standard import standard_bp
from blueprints.charts import charts_bp
from blueprints.data import data_bp

app = Flask(__name__, static_folder='static')

app.register_blueprint(standard_bp, url_prefix="/")
app.register_blueprint(charts_bp, url_prefix="/charts")
app.register_blueprint(charts_bp, url_prefix="/data")

@app.route('/')
def home():
    return render_template('static/home.html')

                       
if __name__ == '__main__':
    app.run(debug=True)

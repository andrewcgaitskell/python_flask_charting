from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import io

import base64
import json

import pandas as pd

# for legend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/plot/<int:id>')
def plot(id):
    dataset_json = [
      {
        "id": 1,
        "product_name": "Product A",
        "sales": {
          "January": 120,
          "February": 150,
          "March": 130,
          "April": 170,
          "May": 160,
          "June": 180
        }
      },
      {
        "id": 2,
        "product_name": "Product B",
        "sales": {
          "January": 80,
          "February": 95,
          "March": 100,
          "April": 110,
          "May": 105,
          "June": 115
        }
      },
      {
        "id": 3,
        "product_name": "Product C",
        "sales": {
          "January": 200,
          "February": 220,
          "March": 210,
          "April": 230,
          "May": 240,
          "June": 250
        }
      }
    ]
    
    # Load the JSON data
    data_df_json = pd.DataFrame(data=dataset_json)
    
    # Flatten the nested 'sales' dictionary
    #df = pd.json_normalize(data_df_json.to_dict(orient='records'), record_path=['sales'], 
    #                      meta=['id', 'product_name'], meta_prefix=None)
    df = pd.json_normalize(data_df_json.to_dict(orient='records'))

    column_names = list(df.columns)
    column_names.remove('id')
    column_names.remove('product_name')

    dataset = pd.melt(df, id_vars=['id','product_name'], value_vars=column_names)

    #print(dataset)
  
    # Step 2: Filter the dataset
    filtered_data = dataset[dataset['id'] == id]

    print(filtered_data)

    if filtered_data.empty:
        return "No data found for the given ID.", 404

    # Step 3: Create the chart using Matplotlib
    plt.figure()
    filtered_data.plot(kind='bar')  # Customize this plot as per your dataset
    plt.title(f'Data for ID {id}')
    plt.xlabel('X-Axis Label')  # Adjust label based on your data
    plt.ylabel('Y-Axis Label')  # Adjust label based on your data

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Step 4: Render the plot in the Jinja2 template
    return render_template('charts/data_plot.html', plot_url=plot_url)

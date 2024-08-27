from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Fetch the model schema from FastAPI
def get_model_schema(model_name: str):
    response = requests.get(f"http://127.0.0.1:8000/model/{model_name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Generate form data from the model schema
def generate_form_data_from_schema(schema: dict):
    form_data = {}
    properties = schema.get("properties", {})
    for field_name, field in properties.items():
        form_data[field_name] = {
            "label": field.get("title", field_name.capitalize()),
            "type": "text" if field.get("type") == "string" else "number",
            "value": ""
        }
    return form_data

@app.route('/edit/<model_name>', methods=['GET', 'POST'])
def edit_model(model_name):
    schema = get_model_schema(model_name)
    if not schema:
        return "Model not found", 404

    if request.method == 'POST':
        # Handle form submission here
        data = request.form.to_dict()
        # You can validate this data or send it back to the FastAPI server
        return "Form submitted successfully!"

    form_data = generate_form_data_from_schema(schema)
    return render_template('form_template.html', form_data=form_data, action=f'/edit/{model_name}')

if __name__ == '__main__':
    app.run(debug=True)

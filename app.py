import os
import uuid
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
data_directory = "data"

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'Invalid JSON data.'}), 400

        url = json_data.get('url')
        response_data = json_data.get('response')

        if not url or not response_data:
            return jsonify({'error': 'URL and response data are required.'}), 400

        file_name = str(uuid.uuid4()) + '.json'
        file_path = os.path.join(data_directory, file_name)
        if url and response_data:
            def dynamic_endpoint():
                return jsonify(response_data)

            app.add_url_rule(url, view_func=dynamic_endpoint)
        with open(file_path, 'w') as file:
            json.dump(json_data, file)

        return jsonify({'message': f'Successfully uploaded {file_name}.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def load_json_files():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    json_files = [f for f in os.listdir(data_directory) if f.endswith(".json")]

    for file_name in json_files:
        try:
            file_path = os.path.join(data_directory, file_name)
            with open(file_path, 'r') as file:
                json_data = json.load(file)

            url = json_data.get('url')
            response_data = json_data.get('response')

            if url and response_data:
                def dynamic_endpoint():
                    return jsonify(response_data)

                app.add_url_rule(url, view_func=dynamic_endpoint)
        except Exception as e:
            print(f"Error loading JSON file '{file_name}': {str(e)}")


@app.route('/get/<string:file_name>', methods=['GET'])
def get(file_name):
    file_path = os.path.join(data_directory, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return jsonify({'data': json_data}), 200
    else:
        return jsonify({'error': 'File not found.'}), 404


if __name__ == '__main__':
    load_json_files()
    app.run(debug=True)

import re
import pandas as pd


from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

@swag_from('docs/text_processing_file.yml', methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():
    # Upload file
    file = request.files.getlist('file')[0]

    # transform file csv ke dataframe
    df = pd.read_csv(file, encoding='latin-1')

    cleaned_text = []
    for text in df['Tweet']:
        cleaned_text.append(re.sub(r'[^a-zA-Z0-9]', ' ', text))
    
    df['cleaned_text'] = cleaned_text

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()
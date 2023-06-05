# import function
import re
import pandas as pd
import function

from flask import Flask, jsonify

# read data
data = pd.read_csv("data.csv")
data = pd.read_csv("data2.csv")
data = pd.read_csv("data3.csv")
data = pd.read_csv("data4.csv")

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

# Swagger Template
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
# End swagger template

# Function cleansing data
def lowercase(text):
        return text.lower()

def hapus_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
    return text

def hapus_unnecessary_char(text):
        text = re.sub('\n',' ',text) # Hapus Setiap enter '\n'
        text = re.sub('rt',' ',text) # Hapus setiap simbol retweet RT
        text = re.sub('user',' ',text) # Hapus setiap username
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Hapus setiap URL
        text = re.sub('  +', ' ', text) # Hapus double space

def preproces(text):
    text = lowercase(text)
    text = hapus_nonaplhanumeric(text)
    text = hapus_unnecessary_char(text)
# End function

# endpoint from user input
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text),
    }

    response_data = jsonify(json_response)
    return response_data
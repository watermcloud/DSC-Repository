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

def learning_form_data():
    # baca setiap kata abusive dan kamusalay
    abusive_df = pd.read_csv('../../Challange GOLD/abusive.csv')
    alay_df = pd.read_csv('../../Challange GOLD/new_kamusalay.csv', encoding='latin-1', header=None)
    alay_df = alay_df.rename(columns={0: 'original', 
                                      1: 'replacement'})

    # baca setiap kata di abusive menjadi list
    abusive_arr = []
    abusive_df_map = abusive_df['ABUSIVE'].tolist()
    print("abusive list:", abusive_df_map)

    # baca setiap kata di kamusalay menajadi list
    alay_df_map = dict(zip(alay_df['original'], alay_df['replacement']))
    print("alay list:", alay_df_map)

    def lowercase(text):
        return text.lower()

    def hapus_unnecessary_char(text):
        text = re.sub('\n',' ',text) # Hapus Setiap enter '\n'
        text = re.sub('rt',' ',text) # Hapus setiap simbol retweet RT
        text = re.sub('user',' ',text) # Hapus setiap username
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Hapus setiap URL
        text = re.sub('  +', ' ', text) # Hapus double space
        return text
        
    def hapus_nonaplhanumeric(text):
        text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
        return text

    def normalisasi_alay(text):
        return ' '.join([alay_df_map[alay_list] if alay_list in alay_df_map else alay_list for alay_list in text.split(' ')])

    def hapus_abusive(text):
        for word in abusive_arr:
            text = text.replace(word, "")
        return text

    def hapus_emoticon_byte(text):
        text = text.replace("\\", " ")
        text = re.sub('x..', ' ', text)
        text = re.sub(' n ', ' ', text)
        text = re.sub('\\+', ' ', text)
        text = re.sub('  +', ' ', text)
        return text
    
    def preprocess(text):
        text = lowercase(text) # aturan 1
        text = hapus_nonaplhanumeric(text) # aturan 2
        text = hapus_unnecessary_char(text) # aturan 2
        text = normalisasi_alay(text) # aturan 3
        text = hapus_abusive(text) # aturan 4
        return text



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

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file)

    # Ambil teks yang akan diproses dalam format list
    # texts = df.text.to_list()

    # Lakukan cleansing pada teks
    cleaned_text = []
    for text in df["Tweet"]:
        cleaned_text.append(re.sub(r'[^a-zA-Z0-9]', ' ', text))

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()
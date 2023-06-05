import pandas as pd
import re

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


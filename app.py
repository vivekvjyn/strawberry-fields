import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import utils

import matplotlib.pyplot as plt

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db = client["MusicCatalog"]
        collection = db["MusicCatalog"]

        y, sr = utils.parse_req(request=request)

        S, onsets, fft_size = utils.stft(y, sr)

        #plt.plot(utils.peak_eval(S, onsets, sr, fft_size))
        #plt.plot(utils.pyin(y, sr), c='r')
        #plt.savefig('plot.png')

        vec1 = utils.hz_to_midi(utils.peak_eval(S, onsets, sr, fft_size))

        #results = ([collection.find()[0], collection.find()[1]], utils.dtw(collection, vec2, int(1.12 * len(vec2)), 5))
        results = utils.dtw(collection, vec1, int(1.12 * len(vec1)), len(vec1) // 12)

        return render_template('results.html', results=results)
    
    else: return render_template('index.html')
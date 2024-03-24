from dotenv import load_dotenv
import os

from flask import Flask, render_template, request, send_file
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import numpy as np
from fastdtw import fastdtw

import utilities as utils

import matplotlib.pyplot as plt 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=["POST"])
def process():
    db = client["MusicCatalog"]
    collection = db["MusicCatalog"]

    signal = np.array([float(x) for x in request.form['signal'].split(',')])

    sample_rate = int(request.form['sample-rate'])

    signal = signal / np.max(abs(signal))

    spectrogram = utils.stft(signal, sample_rate)

    #plt.pcolormesh(spectrogram.T)
    #plt.plot(spectrogram[50])
    #plt.plot(interpolated_peaks, c='r')
    #plt.savefig('plot.png')

    interpolated_peaks = utils.extract_melody(spectrogram)

    fundamental_frequencies = interpolated_peaks * sample_rate / 8192

    #plt.pcolormesh(spectrogram.T)
    #plt.plot(spectrogram[50])
    #plt.plot(interpolated_peaks, c='r')
    #plt.savefig('plot.png')

    #return send_file('plot.png')

    input_melody = 69 + 12 * np.log2((fundamental_frequencies + 0.0001) / 440)

    input_melody = input_melody - np.mean(input_melody)

    window_length = int(1.2 * len(input_melody))
    hop_length = len(input_melody) // 8

    max_similarity = -np.inf
    for document in collection.find():
        current_melody = np.array(document["melody"])

        window_index = 0
        min_distance = np.inf

        while window_index < len(current_melody) - window_length:
            window = current_melody[window_index: window_index + window_length]
            window = window - np.mean(window)

            distance = fastdtw(input_melody, window)[0]

            min_distance = min(distance, min_distance)

            window_index += hop_length

        similarity = 1 / min_distance

        if max_similarity < similarity:
            max_similarity = similarity
            result = {
                "title": document["title"],
                "album": document["album"],
                "singer": document["singer"],
                "composer": document["composer"],
                "lyricist": document["lyricist"],
                "link": document["link"]
            }

    return render_template('result.html', result=result)



from dotenv import load_dotenv
import os

from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import numpy as np
from scipy.io import wavfile
from fastdtw import fastdtw

from short_time_fourier_transform import compute_spectrogram
from peak_detection import estimate_peaks, detectRealpeaks, peakInterpolation

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods =["POST"])
def process():
    file = request.files['audio']

    db = client["MusicCatalog"]

    collection = db["MusicCatalog"]
    
    sampleRate, audio = wavfile.read(file)

    audio = audio / np.max(abs(audio))

    spectrogram = compute_spectrogram(audio, sampleRate)

    peak_frequencyBins, peak_magnitudes = estimate_peaks(spectrogram)

    peak_frequencyBins, peak_magnitudes = detectRealpeaks(spectrogram, peak_frequencyBins, peak_magnitudes)

    peak_frequencyBins, peak_magnitudes = peakInterpolation(spectrogram, peak_frequencyBins, peak_magnitudes)

    input_melody = np.round(69 + 12 * np.log2((peak_frequencyBins + 0.0001) / 440))
    input_melody = input_melody - int(np.mean(input_melody))
    
    window_length = int(2 * len(input_melody))
    hop_length = len(input_melody)

    largest_similarity = -np.inf
    songid = None
    for document in collection.find():
        current_melody = np.array(document["melody"])

        windowIndex = 0
        smallest_distance = np.inf

        while windowIndex < len(current_melody) - window_length:
            window = current_melody[windowIndex: windowIndex + window_length]
            window = window - int(np.mean(window))

            distance, path = fastdtw(input_melody, window)

            smallest_distance = min(distance, smallest_distance)

            windowIndex += hop_length

        similarity = 1 / smallest_distance

        if largest_similarity < similarity:
            largest_similarity = similarity
            song = {
                "title": document["title"],
                "album": document["album"],
                "composer": document["composer"],
                "lyricist": document["lyricist"],
                "singer": document["singer"],
                "link": document["link"],
            }
        

    return render_template('result.html', song=song)


if __name__ == '__main__':
    app.run()
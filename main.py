from dotenv import load_dotenv
import os

from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import numpy as np
from fastdtw import fastdtw

from utilities import calculate_stft, interpolate_peak
from peak_detection import estimate_peaks, detect_real_peaks

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

    spectrogram = calculate_stft(signal, sample_rate)

    peak_frequency_bins, peak_magnitudes = estimate_peaks(spectrogram)

    peak_frequency_bins, peak_magnitudes = detect_real_peaks(spectrogram, peak_frequency_bins, peak_magnitudes)

    interpolated_peaks = interpolate_peak(spectrogram, peak_frequency_bins)

    fundamental_frequencies = interpolated_peaks * sample_rate / 8192

    input_melody = 69 + 12 * np.log2((fundamental_frequencies + 0.0001) / 440)

    input_melody = input_melody - np.mean(input_melody)

    window_length = int(len(input_melody))
    hop_length = len(input_melody) // 8

    max_similarity = -np.inf
    for document in collection.find():
        current_melody = np.array(document["melody"])

        starts = np.arange(0, len(current_melody) - window_length + 1, hop_length)
        windows = np.stack([current_melody[start:start + window_length] for start in starts])

        distances = np.array([fastdtw(input_melody, window)[0] for window in windows])
        min_distance = np.min(distances)

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

if __name__ == '__main__':
    app.run()

from dotenv import load_dotenv
import os

from flask import Flask, render_template, request, send_file
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import numpy as np
from scipy.io import wavfile
from fastdtw import fastdtw

from ultilities import stft, peak_interpolation
from peak_detection import estimate_peaks, detectRealpeaks

import matplotlib.pyplot as plt
import json

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
    db = client["MusicCatalog"]
    collection = db["MusicCatalog"]
    
    file = request.files['audio']
    sampleRate, signal = wavfile.read(file)
    signal = signal / np.max(abs(signal))

    spectrogram = stft(signal, sampleRate)

    

    peak_frequencyBins, peak_magnitudes = estimate_peaks(spectrogram)

    peak_frequencyBins, peak_magnitudes = detectRealpeaks(spectrogram, peak_frequencyBins, peak_magnitudes)

    interpolated_peaks = peak_interpolation(spectrogram, peak_frequencyBins)

    fundamentalfrequencies = interpolated_peaks * sampleRate / 8192

    
    

    input_melody = np.round(69 + 12 * np.log2((peak_frequencyBins + 0.0001) / 440))

    #plt.pcolormesh(spectrogram.T)
    #plt.plot(peak_frequencyBins)
    #plt.plot(440 * 2 ** ((input_melody - 69) / 12))
    

    input_melody = input_melody - np.round(np.mean(input_melody))
    
    window_length = int(2 * len(input_melody))
    hop_length = len(input_melody) // 2

    

    largest_similarity = -np.inf
    smallestpath = None
    for document in collection.find():
        current_melody = np.array(document["melody"])

        windowIndex = 0
        smallest_distance = np.inf

        while windowIndex < len(current_melody) - window_length:
            window = current_melody[windowIndex: windowIndex + window_length]
            window = window - int(np.mean(window))

            distance, path = fastdtw(input_melody, window)

            if distance < 1 / largest_similarity and smallest_distance > distance:
                smallestpath = path
                match = window
                tit = document["title"]

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
    
    colors = ['g', 'm', 'c', 'y', 'k', 'orange', 'purple', 'pink']

    x, y = zip(*smallestpath)

    for i, j in zip(x, y):
        plt.plot([i, j], [input_melody[i], match[j] + 20], '--', c=colors[i%len(colors)])

    plt.plot(input_melody, label='Input Notes', color='blue')
    plt.plot(np.array(match) + 20, label='Database', color='red')
    plt.xlabel(tit)

    plt.savefig("spec.png")
    return send_file("spec.png")
        

    return render_template('result.html', song=song)


if __name__ == '__main__':
    app.run()
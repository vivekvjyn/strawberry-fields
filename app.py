from flask import Flask, render_template, request, send_file
import numpy as np
from scipy.io import wavfile

from spectrogram import computeSpectrogram

import matplotlib.pyplot as plt
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods =["POST"])
def process():
    file = request.files['input']

    sampleRate, audio = wavfile.read(file)
    

    audio = audio / np.max(abs(audio))

    spectrogram = np.array(computeSpectrogram(audio, sampleRate))

    plt.pcolormesh(spectrogram.T)

    plt.savefig('spectrogram.png')

    return send_file('spectrogram.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()
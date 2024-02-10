from flask import Flask, render_template, request, send_file
import numpy as np
from scipy.io import wavfile

from stft import compute_spectrogram
from peak_detection import detect_peaks

import matplotlib.pyplot as plt

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

    spectrogram = compute_spectrogram(audio, sampleRate)

    peak_frequencies, peak_magnitudes = detect_peaks(spectrogram, sampleRate)

    timeSteps = np.arange(len(spectrogram)) * 2048 / sampleRate
    frequencies = np.arange(len(spectrogram[0])) * sampleRate / 8192
    plt.pcolormesh(timeSteps, frequencies, spectrogram.T)
    plt.plot(timeSteps, [p[0] for p in peak_frequencies], c='r')
    plt.plot(timeSteps, [p[1] for p in peak_frequencies], c='b')

    plt.savefig('spectrogram.png')

    #return str(len(peak_frequencies) - len(spectrogram))
    return send_file('spectrogram.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()
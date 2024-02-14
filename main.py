from flask import Flask, render_template, request, send_file
import numpy as np
from scipy.io import wavfile

from stft import compute_spectrogram
from peak_detection import estimate_peaks, detectRealpeaks, peakInterpolation
from two_way_mismatch import calculate_fundamental_frequencies

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

    peak_frequencyBins, peak_magnitudes = estimate_peaks(spectrogram)

    peak_frequencyBins, peak_magnitudes = detectRealpeaks(spectrogram, peak_frequencyBins, peak_magnitudes)

    peak_frequencyBins, peak_magnitudes = peakInterpolation(spectrogram, peak_frequencyBins, peak_magnitudes)

    fundamentalFrequencies = calculate_fundamental_frequencies(peak_frequencyBins * sampleRate / 8192, peak_magnitudes)

    timeSteps = np.arange(len(spectrogram)) * 2048 / sampleRate
    frequencies = np.arange(len(spectrogram[0])) * sampleRate / 8192
    plt.pcolormesh(timeSteps, frequencies, spectrogram.T)
    plt.plot(timeSteps, fundamentalFrequencies, c='r')
    #plt.plot(timeSteps, [p[1] for p in peak_frequencyBins * sampleRate / 8192], c='b')

    plt.savefig('spectrogram.png')

    #return str(fundamentalFrequencies)
    return send_file('spectrogram.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()
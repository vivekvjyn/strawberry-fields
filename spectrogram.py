import math
import numpy as np
from scipy.signal import get_window
from scipy.fft import fft

windowSize = 8191
fftBufferSize = 8192
hopLength = 2048

hM1 = int(math.floor((windowSize + 1) / 2))
hM2 = int(math.floor(windowSize / 2))
epsilon = np.finfo(float).eps

window  = get_window('hamming', windowSize)
window = window / sum(window)

def computeSpectrogram(audio, sampleRate):
    cutoffFrequency = int(1000 * fftBufferSize / sampleRate)

    spectrogram = []
    
    l = 0
    while l < len(audio) - windowSize:
        frame = audio[l: l + windowSize]
        
        rms = np.sqrt(np.dot(frame, frame) / windowSize)    
        
        if rms > 0.1:
            frame = frame / np.max(abs(frame))
            frame = frame * window

            fftBuffer = np.zeros(fftBufferSize)
            fftBuffer[: hM1] = frame[hM2:] 
            fftBuffer[fftBufferSize - hM2:] = frame[: hM2]

            spectrum = fft(fftBuffer)
            magnitudeSpectrum = abs(spectrum)
            magnitudeSpectrum[magnitudeSpectrum < epsilon] = epsilon
            logMagnitudeSpectrum = 10 * np.log10(magnitudeSpectrum)

            spectrogram.append(logMagnitudeSpectrum[:cutoffFrequency])

        l += hopLength
    
    return spectrogram
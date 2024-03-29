from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import utils as ut

import matplotlib.pyplot as plt

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        db = client["MusicCatalog"]
        collection = db["MusicCatalog"]

        x, sr = ut.parse(request.form)

        stft, t_onset, n_fft = ut.stft(x, sr)
        f0_stft = ut.local_max(stft, t_onset, sr, n_fft)
        midi_stft = ut.midi(f0_stft)

        win_length_stft = int(1.12 * len(midi_stft))
        hop_length_stft = len(midi_stft) // 8
        meta_stft = ut.dtw(collection, midi_stft, win_length_stft, hop_length_stft)

        f0_pyin = ut.pyin(x, sr)
        midi_pyin = ut.midi(f0_pyin)

        win_length_pyin = int(1.12 * len(midi_pyin))
        hop_length_pyin = len(midi_pyin) // 8
        meta_pyin = ut.dtw(collection, midi_pyin, win_length_pyin, hop_length_pyin)

        plt.pcolormesh(stft.T)
        plt.plot(f0_stft * n_fft / sr, c='g')
        plt.plot(f0_pyin * n_fft / sr, c='r')
        plt.savefig('plot.png')

        return render_template('output.html', meta_stft=meta_stft, meta_pyin=meta_pyin)
    else:
        return render_template('input.html')
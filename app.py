import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import utils

import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Set maximum content length for file uploads
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

# Initialize MongoClient with server API version 1
uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/', methods=["GET", "POST"])
def index():
    """
    Handle requests for song retrieval by hummed query.
    """
    if request.method == "POST":
        # Access MusicCatalog database
        db = client["MusicCatalog"]
        collection = db["MusicCatalog"]

        # Parse signal and samplerate from the request
        y, sr = utils.parse_req(request=request)

        # Compute STFT
        S, onsets, fft_size = utils.stft(y, sr)

        # Extract pitch vector from peaks in STFT
        peaks = utils.find_peaks(S, onsets, sr, fft_size)

        plt.pcolormesh(S.T)
        plt.plot(peaks * fft_size / sr, c='r')
        plt.savefig('plot.png')

        vector = utils.hz_to_midi(peaks)

        # Perform DTW on music catalog database
        results = utils.dtw(collection, vector, int(1.12 * len(vector)), len(vector) // 12)

        # Render results template with top matching songs
        return render_template('results.html', results=results)
    
    else: 
        # Render index template for query submission
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
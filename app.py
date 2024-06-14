import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import utils

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/', methods=["GET", "POST"])
def index():
    """
    Handle requests for song retrieval by hummed query.
    """
    if request.method == "POST":
        db = client["MusicCatalog"]
        collection = db["MusicCatalog"]

        y, sr = utils.parse_request(request)
        f0 = utils.pyin(y, sr)
            
        note_nums = utils.hz_to_midi(f0)

        candidates = utils.knn(collection, note_nums)

        results = utils.dtw(candidates, note_nums, int(1.12 * len(note_nums)), len(note_nums) // 12)

        return render_template('results.html', results=results)
    
    else: 
        # Render index template for query submission
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
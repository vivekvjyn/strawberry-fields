import os
import numpy as np
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tslearn.neighbors import KNeighborsTimeSeries

load_dotenv()

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["MusicCatalog"]
collection = db["MusicCatalog"]

dataset = []
window_size = 300
hop_length = window_size // 8
idx = 0
for document in collection.find():
    vector = document["vector"]
    
    hashes = []
    for l in range(0, len(vector) - window_size, hop_length):
        Y = vector[l: l + window_size]
        Y = Y - np.mean(Y)
        
        hashes.append(idx)
        idx += 1

        dataset.append(Y)
    
    collection.update_one({'title': document["title"]}, {'$set': {'hashes': hashes}})

knn = KNeighborsTimeSeries(n_neighbors=10, metric='dtw')
knn.fit(dataset)

knn.to_json('model.json')

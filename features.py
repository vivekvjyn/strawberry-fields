from mido import MidiFile
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

def extract_vec(path='midi.mid', sr=48000, hop_length=2048):
    midi = MidiFile(path)

    vector = []

    for message in midi.play():
        if message.type == 'note_off':
            time = message.time
            note = message.note
            
            for i in range(int(time * sr / hop_length)):
                vector.append(note)

    return vector

uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.vultpjd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["MusicCatalog"]
collection = db["MusicCatalog"]


title = input('Title: ')
album = input('Album: ')
singer = input('Singer: ')
composer = input('Composer: ')
lyricist = input('Lyricist: ')
link = input('Link: ')

sr=48000
hop_length=2048

midi = MidiFile(input('MIDI file path: '))

vector = []

for message in midi.play():
    if message.type == 'note_off':
        time = message.time
        note = message.note
        
        for i in range(int(time * sr / hop_length)):
            vector.append(note)

data = {
    "title": title,
    "album": album,
    "singer": singer,
    "composer": composer,
    "lyricist": lyricist,
    "link": link,
    "vector": vector
}

collection.insert_one(data)


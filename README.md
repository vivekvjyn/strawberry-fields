# Strawberry fields
Song retrieval using hummed query

## Setup
**Clone the Repository:**
```bash
git clone https://github.com/enter-opy/strawberry-fields.git
cd sound-of-music
```
### Environment setup.
Create a virtual environment.
```bash
pip install virtualenv
virtualenv venv
```
Activate your environment.

   **Windows:**
```bash
venv\Scripts\activate
```

   **Linux:**
```bash
source venv/bin/activate
```
Create a `.env` file in the root directory of your project and copy the following into the file:

```makefile
USER=username
PASSWORD=password
SECRET_KEY=secret_key
```
Replace username, password, and secret_key with your actual MongoDB username, password, and Flask secret key

### Install Dependencies

Install the required packages using pip with the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage
### MongoDB Setup

Ensure you have MongoDB installed and running. Create a database named `MusicCatalog` and a collection named `MusicCatalog`.

The collection should have the following attributes.

```json
{
   "title": "Song name",
   "album": "Album name",
   "singer": "Singer(s)",
   "composer": "Composer(s)",
   "lyricist": "Lyricist(s)",
   "link": "Link to the song in a streaming platform",
   "vector": [],
   "hashes": []
}
```

### Pitch vectors
Extract pitch vectors from MIDI files of your desired songs and add to the `hashes` of your MongoDB collection appropriatly.

You can use [mido](https://mido.readthedocs.io/en/stable/) for this task.

### Training the model

Retrive the pitch vectors and divide it into into equal overlapping segments into an [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html).

Follow instructions in [tslearn documentation](tslearn.neighbors.KNeighborsTimeSeries) to train a tslearn.neighbors.KNeighborsTimeSeries model on the numpy.ndarray and save the model to `model.json`. Store the indices appropriatly to the `hashes` of your MongoDB collection. 

### Run the application

```bash
python -m flask run
```


### References

- Joan Serrà, Josep Ll. Arcos, *An Empirical Evaluation of Similarity Measures for Time Series Classification*, Jan 2014.
- Hiroaki Sakoe, Seibi Chiba, *Dynamic programming algorithm optimization for spoken word recognition*, February 1978.
- Ivan Fernandez Cocano, *Expanding the evaluation of Audio to Score Matching applying Audio Querying strategies*, August 2023.
- Colin Raffel, Daniel P. W. Ellis, *Large-Scale Contend-Based Matching of Midi and Audio Files*, January 2015.
- Matija Marolt, *A mid level melody based representation for calculating audio similarity*, January 2006.
- Matthias Mauch and Simon Dixon, *PYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold Distributions*, May 2014.
- Neal Gallagher, *Savitzky-Golay Smoothing and Differentiation Filter*, January 2020.
- Pedro Cano, Eloi Batlle, *A Review of Audio Fingerprinting*, November 2005.
- Pavel Senin, *Dynamic Time Warping Algorithm Review*, January 2009.
- Tomasz Górecki, Maciej Łuczak, *The influence of the Sakoe–Chiba band size on time series classification*, January 2019.

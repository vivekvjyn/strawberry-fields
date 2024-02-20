const recordButton = document.querySelector("#record-button");
const audio = document.querySelector("#audio");
const file = document.querySelector("#file");

recordButton.addEventListener("click", toggleMicrophone);

let canRecord = false;
let isRecording = false;

let meadiaRecorder = null;

let chunks = [];

function setupAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            audio: true
        })
        .then(setupStream)
        .catch(err => {
            console.error(err)
        })
    }
}

setupAudio();

function sentAudio(blob) {
    var formData = new FormData();
    formData.append('file', blob, 'data.wav');
    formData.append('title', 'data.wav');

    $.ajax({
        type: 'POST',
        url: '/process',
        data: formData,
        cache: false,
        processData: false,
        contentType: false
    }).done(function(blob) {
        console.log(blob);
    });
}

function setupStream(stream) {
    meadiaRecorder = new MediaRecorder(stream);

    meadiaRecorder.ondataavailable = event => {
        chunks.push(event.data);
    }

    meadiaRecorder.onstop = () => {
        const blob = new Blob(chunks, {type: "audio/wav; codecs=opus"});
        chunks = [];
        audioURL = URL.createObjectURL(blob);

        sentAudio(blob)

        audio.src = audioURL
    }

    canRecord = true;
}

function toggleMicrophone() {
    if (!canRecord) return;

    isRecording = !isRecording;

    if (isRecording) {
        meadiaRecorder.start();
    }

    else {
        meadiaRecorder.stop();
    }
}
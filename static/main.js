document.getElementById("recordButton").addEventListener("click", startRecording);

let mediaRecorder = null;
let canRecord = false;
let isRecording = false;
let recordedChunks = [];

function initializeAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(handleStream)
            .catch(handleError);
    }
}

initializeAudio();

function handleStream(stream) {
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
        recordedChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(recordedChunks, { type: "audio/wav" });
        recordedChunks = [];
        const reader = new FileReader();
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        reader.onload = () => {
            const arrayBuffer = reader.result;
            audioContext.decodeAudioData(arrayBuffer, decodedAudio => {
                const channelData = Array.from(decodedAudio.getChannelData(0));
                document.getElementById("signal").value = channelData;
                document.getElementById("sampleRate").value = audioContext.sampleRate;
                document.getElementById("form").submit();
            });
        };
        reader.readAsArrayBuffer(audioBlob);
    };

    canRecord = true;
}

function startRecording() {
    if (!canRecord) return;

    isRecording = !isRecording;

    if (isRecording) {
        mediaRecorder.start();
        document.getElementById("recordButton").classList.toggle("glow-animation");

        setTimeout(() => {
            var button = document.getElementById("recordButton");
            button.classList.remove("glow-animation")
            button.disabled = true;

            mediaRecorder.stop();
        }, 15000);
    } else {
        location.reload();
    }
}

function handleError(error) {
    console.error("Error accessing user media:", error);
}

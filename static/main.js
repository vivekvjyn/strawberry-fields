// Add event listener to the button
document.getElementById("recordButton").addEventListener("click", toggleRecording);

let mediaRecorder = null;
let canRecord = false;
let isRecording = false;
let recordedChunks = [];

function initializeAudio() {
    // Check if getUserMedia is supported by the browser
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(handleStream)
            .catch(handleError);
    }
}

initializeAudio();

function handleStream(stream) {
    // Create a new MediaRecorder object with the audio stream
    mediaRecorder = new MediaRecorder(stream);

    // Push the recorded audio data to the array when data is available
    mediaRecorder.ondataavailable = event => {
        recordedChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        // Create a blob from the recorded chunks
        const audioBlob = new Blob(recordedChunks, { type: "audio/wav" });
        recordedChunks = [];

        const reader = new FileReader();
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Read the audio blob as an array buffer
        reader.onload = () => {
            const arrayBuffer = reader.result;
            audioContext.decodeAudioData(arrayBuffer, decodedAudio => {
                const channelData = Array.from(decodedAudio.getChannelData(0));

                // Set the signal input values and submit the input form
                document.getElementById("signal").value = channelData;
                document.getElementById("sampleRate").value = audioContext.sampleRate;
                document.getElementById("form").submit();
            });
        };
        reader.readAsArrayBuffer(audioBlob);
    };

    canRecord = true;
}

function toggleRecording() {
    if (!canRecord) return;

    isRecording = !isRecording;

    // Start or stop recording based on the recording flag
    if (isRecording) {
        mediaRecorder.start();

        document.getElementById("recordButton").classList.toggle("glow-animation");

        // Automatically stop recording after 8 seconds
        setTimeout(() => {
            document.getElementById("recordButton").classList.toggle("glow-animation");

            mediaRecorder.stop();
        }, 8000);
    } else {
        document.getElementById("recordButton").classList.toggle("glow-animation");

        mediaRecorder.stop();
    }
}

function handleError(error) {
    console.error("Error accessing user media:", error);
}

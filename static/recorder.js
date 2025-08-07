const record = document.querySelector('.record');

// check if the browser supports getUserMedia API
if (navigator.mediaDevices.getUserMedia) {

    // if media setup is successful, recording starts
    let onMediaSetupSuccess = function (stream) {
        alert('Media setup successful!');
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        // on click event, start or stop recording
        record.onclick = function () {
            if (mediaRecorder.state === "recording") {
                mediaRecorder.stop();
                record.classList.remove('recording'); // Remove red background
                record.textContent = 'Start Recording';
            } else {
                mediaRecorder.start();
                record.classList.add('recording'); // Add red background
                record.textContent = 'Stop Recording';
            }
        }

        // on data available, store the audio chunks
        mediaRecorder.ondataavailable = function (event) {
            audioChunks.push(event.data);
        }

        // on stop event, create a Blob from the audio chunks and send it to the server
        mediaRecorder.onstop = function () {
            let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            chunks = [];
            let formData = new FormData();
            formData.append('file', audioBlob);

            fetch("/transcribe", {
                method: 'POST',
                body: formData
            }).then((response) => response.text())
                .then((html) => {
                    document.open();
                    document.write(html);
                    document.close();
                })
        }
    }

    // if media setup fails, alert the user
    let onMediaSetupFailure = function (err) {
        alert('Media setup failed: ' + err.name + ' - ' + err.message);
    }

    // request access to the user's microphone
    navigator.mediaDevices.getUserMedia({ audio: true }).then(onMediaSetupSuccess).catch(onMediaSetupFailure);

} else { // if getUserMedia is not supported, alert the user
    alert('getUserMedia not supported on your browser!');
}
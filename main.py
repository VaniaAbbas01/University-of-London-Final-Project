from flask import Flask, render_template, request, Response, redirect, url_for
import cv2
import json
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_here'
camera = cv2.VideoCapture(0)

# defining extensions for video files
ALLOWED_EXTENSIONS = {'mp4', 'mp3'}

# Dummy feedback data (simulating model output)
mock_feedback = {
    "transcription": "Hello everyone, thank you for joining this session. I would like to talk about...",
    "fluency": {
        "words_per_minute": 130,
        "filler_words": 3,
        "pauses": 5
    },
    "tone": [
        {"time": 0, "tone": "Neutral"},
        {"time": 10, "tone": "Nervous"},
        {"time": 20, "tone": "Confident"}
    ],
    "feedback": [
        {"type": "Filler", "word": "um", "suggestion": "Try replacing with a pause."},
        {"type": "Pace", "issue": "Too fast", "suggestion": "Slow down around conclusion."}
    ]
}

# rendering landing page
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")



# checking if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generateFrames():
    while True:
        # read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    
# uploading audio file
@app.route("/upload", methods=["POST"])
def upload():
    if 'audio' not in request.files:
        return redirect(url_for('index'))
    
    # requesting audio file 
    audio = request.files['audio']
    # if no file is selected
    if audio.filename == '':
        return redirect(url_for('index'))
    
    # if file is selected and extension allowed 
    if audio and allowed_file(audio.filename):
        audio.save('static/uploads/' + audio.filename)
        # render feedback page with mock data
        return render_template('feedback.html', filename=audio.filename, feedback=mock_feedback)
    return "invalid file type", 400

# route to the audio file uploaded
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

@app.route("/video")
def video():
    return Response(generateFrames(), mimetype="multipart/x-mixed-replace; boundary=frame")
     

if __name__ == "__main__":
    app.run(debug=True)
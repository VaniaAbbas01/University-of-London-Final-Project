from flask import Flask, render_template, request, Response, redirect, url_for, session, send_from_directory
from models.speech_to_text import loadModel, transcribeAudio
from models.grammar_correction import grammarCorrection, countFillerWords, countWordsPerMinute
from models.speech_to_emotion import predictEmotion
import ffmpeg
import tempfile
# import cv2
import json
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_here'

model = loadModel()

# camera = cv2.VideoCapture(0)

# defining extensions for video files
ALLOWED_EXTENSIONS = {'mp4', 'mp3'}
audioDuration = 0

# rendering landing page
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


def findAudioDuration(audio_path):
    """Get the duration of the audio file in seconds (as float)."""
    try:
        probe = ffmpeg.probe(audio_path)
        duration = float(probe['format']['duration'])
        print(f"{audio_path} - Duration: {duration:.2f} seconds")
        return duration
    except ffmpeg.Error as e:
        print(f"FFmpeg error while getting duration for {audio_path}:\n{e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# checking if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
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
        # save the file to a temporary location
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
            temp_path = temp.name
            # Close the tempfile to ensure it's saved correctly
            temp.close() 
            try:
            # Save the file after closing the tempfile context
                audio.save(temp_path)
                transcription = transcribeAudio(model, temp_path)
                session['audioDuration'] = findAudioDuration(temp_path)
                session['audioPath'] = temp_path
            except Exception as e:
                # Clean up temp file manually
                print(f"Error saving audio file: {e}")
                
        feedback = {
            "transcription": transcription,
            "fluency": {
                "words_per_minute": 0,
                "filler_words": 0,
                "pauses": 0
            },
            "tone": [],
            "feedback": []
        }
        return render_template('transcription.html', feedback=feedback)
    return "invalid file type", 400

# route to correct grammar from transcribed text
@app.route("/correctGrammar", methods=["POST"])
def correctGrammar():
    transcribed_text = request.form.get('transcription')
    if not transcribed_text:
        return "No transcription provided", 400
    corrected_text = grammarCorrection(transcribed_text)
    duration = session.get('audioDuration', 1)
    wpm, pacing_feedback = countWordsPerMinute(corrected_text, duration)
    tone = predictEmotion(session.get('audioPath'))
    feedback = {
        "transcription": corrected_text,
        "fluency": {
            "words_per_minute": wpm,
            "filler_words": countFillerWords(corrected_text),
            "pauses": 0  # Add pause detection if implemented
        },
        "tone": [tone],  # Add tone analysis if needed
        "feedback": [
            {"type": "Pacing", "suggestion": pacing_feedback},
            {"type": "Grammar", "suggestion": "Minor sentence structure improvements made."},
            {"type": "Filler Words", "suggestion": "Try to avoid frequent use of 'um' and 'like'."}
        ]  
    }
    # Clean up temp file here, after it's used
    if session.get('audioPath') and os.path.exists(session.get('audioPath')):
        os.remove(session.get('audioPath'))
        session.pop('audioPath', None)
        session.pop('audioDuration', None)
    return render_template('feedback.html', feedback=feedback)
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route("/video")
# def video():
#     return Response(generateFrames(), mimetype="multipart/x-mixed-replace; boundary=frame")
     

if __name__ == "__main__":
    app.run(debug=True)
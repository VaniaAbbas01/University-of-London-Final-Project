import tempfile, os, json, random
from flask import Blueprint, request, session, redirect, url_for, render_template
from services.audioService import allowed_file, find_audio_duration
from features.speech_to_text import Transcription

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload():
    if 'audio' not in request.files:
        return redirect(url_for('main.index'))
    
    audio = request.files['audio']
    if audio.filename == '':
        return redirect(url_for('main.index'))
    
    if audio and allowed_file(audio.filename, {'mp3','mp4'}):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
            temp_path = temp.name
            audio.save(temp_path)

        transcription = Transcription()
        transcript = transcription.transcribeAudio(temp_path)

        session['audioDuration'] = find_audio_duration(temp_path)
        session['audioPath'] = temp_path

        return render_template('transcription.html', transcription=transcript)
    return "Invalid file type", 400

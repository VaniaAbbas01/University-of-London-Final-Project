import tempfile, os
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
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
    
    if audio and allowed_file(audio.filename, {'mp3', 'mp4'}):
        try:
            # Save temporarily
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
                temp_path = temp.name
                audio.save(temp_path)

            # Run transcription
            transcription_service = Transcription()
            transcript = transcription_service.transcribeAudio(temp_path)

            # Store in session
            session['audioDuration'] = find_audio_duration(temp_path)
            session['audioPath'] = temp_path

            return render_template("transcription.html", transcription=transcript)

        except Exception as e:
            # Clean up file if something fails
            if "temp_path" in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            flash(f"Transcription failed: {str(e)}")
            return redirect(url_for("main.index"))

    return "Invalid file type", 400

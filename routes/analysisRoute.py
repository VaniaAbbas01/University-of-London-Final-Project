import os, json
from flask import Blueprint, request, session, render_template
from services.feedbackService import generate_feedback

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/analyse", methods=["POST"])
def analyse():
    transcribed_text = request.form.get("transcription")
    if not transcribed_text:
        return "No transcription provided", 400
    
    audio_path = session.get("audioPath")
    duration = session.get("audioDuration", 1)

    if not audio_path:
        return "No audio file found in session", 400

    feedback, audio_results = generate_feedback(transcribed_text, audio_path, duration)

    # cleanup temp file
    if audio_path and os.path.exists(audio_path):
        os.remove(audio_path)
        session.pop("audioPath", None)
        session.pop("audioDuration", None)

    return render_template(
        "feedback.html",
        feedback=feedback,
        pitch_series=json.dumps(audio_results.get("pitch_series",[])),
        intensity_series=json.dumps(audio_results.get("intensity_series",[]))
    )

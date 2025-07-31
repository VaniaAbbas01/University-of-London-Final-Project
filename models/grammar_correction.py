from happytransformer import HappyTextToText, TTSettings
import nltk
import re

nltk.download('punkt')
from nltk.tokenize import sent_tokenize


def loadModel():
    """"Load the language model for grammar correction."""
    happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

    args = TTSettings(num_beams=5, min_length=1)

    return happy_tt, args

happy_tt, args = loadModel()

def grammarCorrection(text):
    """Correct grammar in the given text."""
    sentences = sent_tokenize(text)
    result = ""
    for s in sentences:
        corrected = happy_tt.generate_text(s, args=args)
        result += corrected.text + " "

    print(f"Corrected text: {result.strip()}")
    return result.strip()

def countFillerWords(text):
    """Count filler words in the given text."""
    filler_words = ["um", "uh", "like", "you know", "so", "actually"]
    count = 0
    suggestion = ""
    for fw in filler_words:
        # Use regex word boundaries to avoid partial matches (e.g., "some" includes "so")
        pattern = r'\b' + re.escape(fw) + r'\b'
        matches = re.findall(pattern, text)
        count += len(matches)
        
    if count == 0:
        suggestion = "Excellent! You used no filler words. Your speech was clear and confident."
    elif 1 <= count <= 3:
        suggestion = "Good job! You used very few filler words. Try to stay mindful to reduce them further."
    elif 4 <= count <= 7:
        suggestion = "You used a moderate number of filler words. Practice pausing silently instead of saying 'um' or 'like'."
    else:
        suggestion = "You used too many filler words. Work on speaking more deliberately and using pauses to gather your thoughts."

    return count, suggestion

def countWordsPerMinute(text, duration):
    """
    Count words per minute (WPM) and give pacing feedback.
    Returns (wpm, feedback).
    """
    if duration < 10:
        return None, "Audio too short to give pacing feedback."

    words = len(text.split())
    wpm = words / (duration / 60)

    # Feedback based on general public speaking guidelines
    if wpm < 100:
        feedback = "You're speaking too slowly. Try to speak a bit faster."
    elif 100 <= wpm <= 160:
        feedback = "Your pace is good. Keep it up!"
    elif 160 < wpm <= 190:
        feedback = "You're speaking slightly fast. Slow down just a bit."
    else:
        feedback = "You're speaking too fast. Try to slow down."

    return round(wpm, 2), feedback




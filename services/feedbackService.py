from features.grammar_correction import GrammarCorrection
from features.language_analysis import LanguageAnalyser
from features.speech_to_emotion import SpeechToEmotion
from features.audio_analysis import AudioAnalyser

def generate_feedback(transcribed_text, audio_path, duration):
    try:
        # Initialize analyzers
        grammarCorrection = GrammarCorrection()
        languageAnalyser = LanguageAnalyser()
        speechToEmotion = SpeechToEmotion()
        audioAnalyser = AudioAnalyser(audio_path)
        
        # Grammar correction
        corrected_text = grammarCorrection.correctGrammar(transcribed_text)
        
        # Language analysis
        filler_count, filler_suggestion = languageAnalyser.countFillerWords(corrected_text)
        wpm, pacing_feedback = languageAnalyser.countWordsPerMinute(corrected_text, duration)
        vocab_score, vocab_feedback = languageAnalyser.analyseVocabularyRichness(corrected_text)
        
        # Emotion/tone analysis
        tone = speechToEmotion.predictEmotion(audio_path)
        
        # Audio analysis
        audio_results = audioAnalyser.extractFeatures()
        
        # Extract pause information from audio analysis if available
        pause_info = audio_results.get("features", {}).get("pause_ratio", 0)
        
        # Combine audio feedback with other feedback
        audio_feedback = audio_results.get("feedback", {})
        
        # Build comprehensive feedback
        feedback_list = [
            {"type": "Pacing", "suggestion": pacing_feedback},
            {"type": "Grammar", "suggestion": "Minor sentence structure improvements made."},
            {"type": "Filler Words", "suggestion": filler_suggestion},
            {"type": "Vocabulary Richness", "suggestion": vocab_feedback}
        ]
        
        # Add audio-specific feedback
        for category, suggestion in audio_feedback.items():
            feedback_list.append({
                "type": category.capitalize(), 
                "suggestion": suggestion
            })
        
        feedback = {
            "transcription": corrected_text,
            "fluency": {
                "words_per_minute": wpm,
                "filler_words": filler_count,
                "pauses": pause_info,  
                "vocabulary_richness": vocab_score
            },
            "tone": tone,
            "audio": audio_results,
            "feedback": feedback_list
        }
        
        return feedback, audio_results
    
    except Exception as e:
        # Log the error 
        print(f"Error in generate_feedback: {str(e)}")
        
        # Return a basic feedback structure with error indication
        error_feedback = {
            "transcription": transcribed_text,
            "fluency": {
                "words_per_minute": 0,
                "filler_words": 0,
                "pauses": 0,
                "vocabulary_richness": 0
            },
            "tone": "unknown",
            "audio": {"features": {}, "feedback": {}},
            "feedback": [
                {"type": "Error", "suggestion": "Analysis could not be completed. Please try again."}
            ]
        }
        
        return error_feedback, {"features": {}, "feedback": {}}

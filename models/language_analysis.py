import re

class LanguageAnalyser:

    # counts filler words in the given text and gives suggestions accordingly
    def countFillerWords(self, text):
        """Count filler words in the given text."""
        # Define common filler words
        filler_words = ["um", "uh", "like", "you know", "so", "actually"]
        count = 0
        suggestion = ""
        # for every filler word, find all occurrences in the text
        for fw in filler_words:
            # Use regex word boundaries to avoid partial matches (e.g., "some" includes "so")
            pattern = r'\b' + re.escape(fw) + r'\b'
            matches = re.findall(pattern, text)
            count += len(matches)
            
        # suggest based on the count of filler words
        if count == 0:
            suggestion = "Excellent! You used no filler words. Your speech was clear and confident."
        elif 1 <= count <= 3:
            suggestion = "Good job! You used very few filler words. Try to stay mindful to reduce them further."
        elif 4 <= count <= 7:
            suggestion = "You used a moderate number of filler words. Practice pausing silently instead of saying 'um' or 'like'."
        else:
            suggestion = "You used too many filler words. Work on speaking more deliberately and using pauses to gather your thoughts."

        return count, suggestion

    # counts words per minute (WPM) and gives pacing feedback
    def countWordsPerMinute(self, text, duration):
        """
        Count words per minute (WPM) and give pacing feedback.
        Returns (wpm, feedback).
        """
        if duration < 10:
            return None, "Audio too short to give pacing feedback."

        # Count words in the text
        words = len(text.split())
        # Calculate WPM
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
    
    # analyze vocabulary richness using Type-Token Ratio (TTR)
    def analyseVocabularyRichness(self, text):
        """
        Analyze vocabulary richness in the text.
        Returns a score and feedback.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        totalWords = len(words)
        uniqueWords = len(set(words))

        if totalWords == 0:
            return 0.0, "No words found in the input."

        ttr = uniqueWords / totalWords

        # Provide feedback based on TTR range
        if ttr > 0.6:
            feedback = "Excellent vocabulary richness! You used a wide range of words."
        elif 0.4 <= ttr <= 0.6:
            feedback = "Your vocabulary is moderately varied. Consider using more diverse word choices."
        else:
            feedback = "Your vocabulary was quite limited. Try incorporating a broader range of words."

        return round(ttr, 2), feedback
    
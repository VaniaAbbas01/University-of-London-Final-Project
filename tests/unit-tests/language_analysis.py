import unittest
from features.language_analysis import LanguageAnalyser

class TestLanguageAnalyser(unittest.TestCase):

    def setUp(self):
        self.analyser = LanguageAnalyser()

    # --------- FILLER WORDS -------- 
    # test case for no use of filler words
    def test_count_filler_words_none(self):
        """Test lack of use of Filler Words"""
        text = "Hi all. Thank you for coming today."
        count, suggestion = self.analyser.countFillerWords(text)
        self.assertEqual(count, 0)
        self.assertIn("Excellent", suggestion)

    # test case for no few of filler words
    def test_count_filler_words_few(self):
        """Tests Few Filler words"""
        text = "Um I think we should actually go now."
        count, suggestion = self.analyser.countFillerWords(text)
        self.assertEqual(count, 2)  # "Um", "actually"
        self.assertIn("few filler words", suggestion)

    # test case for no heavy of filler words
    def test_count_filler_words_many(self):
        """"Tests Heavy use of Filler Words"""
        text = "Um uh like you know so um uh like actually."
        count, suggestion = self.analyser.countFillerWords(text)
        self.assertGreater(count, 7)
        self.assertIn("too many filler words", suggestion)

    # ------- WORDS PER MINUTE ----------
    # test case for short audio
    def test_wpm_short_audio(self):
        """Test WPM in short audio"""
        text = "This is short."
        wpm, feedback = self.analyser.countWordsPerMinute(text, duration=5)
        self.assertIsNone(wpm)
        self.assertIn("Audio too short", feedback)

    # test case for slow speech
    def test_wpm_slow_speech(self):
        """Test in slow speech"""
        text = "This is a slow speech with very few words."
        wpm, feedback = self.analyser.countWordsPerMinute(text, duration=60)
        self.assertLess(wpm, 100)
        self.assertIn("too slowly", feedback)

    # test case for a good speed
    def test_wpm_good_speed(self):
        """Test WPM in a good audio speech"""
        text = "word " * 120
        wpm, feedback = self.analyser.countWordsPerMinute(text, duration=60)
        self.assertTrue(100 <= wpm <= 160)
        self.assertIn("pace is good", feedback)

    # test case for when the pace is fast
    def test_wpm_too_fast(self):
        """Test for when the pace is fast"""
        text = "word " * 400 
        wpm, feedback = self.analyser.countWordsPerMinute(text, duration=60)  # 1 min
        self.assertGreater(wpm, 190)
        self.assertIn("too fast", feedback)

    # ---------- VOCABULARY RICHNESS ----------
    # test case for empty words
    def test_empty_vocab_richness(self):
        """Tests for empty vocabulary"""
        score, feedback = self.analyser.analyseVocabularyRichness("")
        self.assertEqual(score, 0.0)
        self.assertIn("No words found", feedback)

    # test case for limited richness
    def test_limited_vocab_richness(self):
        """"Tests for limited richness"""
        text = "hello hello hello hello"
        score, feedback = self.analyser.analyseVocabularyRichness(text)
        self.assertLess(score, 0.4)
        self.assertIn("limited", feedback)

    # test case for moderate richness
    def test_moderate_vocab_richness(self):
        """Tests for moderate richness"""
        text = "The the cat cat ran ran"
        score, feedback = self.analyser.analyseVocabularyRichness(text)
        self.assertTrue(0.4 <= score <= 0.6)
        self.assertIn("moderately varied", feedback)

    # test case for heavy vocabulary richness
    def test_high_vocab_richness(self):
        """Tests for heavy richness"""
        text = "The sun shines brightly while the river flows gently across valleys"
        score, feedback = self.analyser.analyseVocabularyRichness(text)
        self.assertGreater(score, 0.6)
        self.assertIn("Excellent vocabulary richness", feedback)


if __name__ == "__main__":
    unittest.main()

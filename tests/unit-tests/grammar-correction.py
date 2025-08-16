import unittest
from features.grammar_correction import GrammarCorrection

grammarCorrection = GrammarCorrection()
class TestGrammarCorrection(unittest.TestCase):

    # setting up GrammarCorrection object
    @classmethod
    def setUpClass(cls):
        """Set up the grammar correction model before any tests."""
        cls.grammarCorrection = GrammarCorrection()

    # testing simple errors 
    def test_correction_of_simple_error(self):
        """Test correcting a basic subject-verb agreement error."""
        input_text = "She go to school every day."
        expected_substring = "She goes to school"
        corrected_text = self.grammarCorrection.correctGrammar(input_text)
        self.assertIn(expected_substring.lower(), corrected_text.lower())

    # testing already corrected errors
    def test_already_correct_sentence(self):
        """Test that a correct sentence is left mostly unchanged."""
        input_text = "He is reading a book."
        corrected_text = self.grammarCorrection.correctGrammar(input_text)
        self.assertEqual(corrected_text.strip(), input_text.strip())

    # testing empty output
    def test_empty_input(self):
        """Test that empty input returns empty output or a graceful fallback."""
        input_text = ""
        corrected_text = self.grammarCorrection.correctGrammar(input_text)
        self.assertTrue(corrected_text == "" or corrected_text.isspace())

    # testing multiple errors 
    def test_multiple_errors(self):
        """Test a sentence with several grammatical issues."""
        input_text = "He don't has no time for go there."
        corrected_text = self.grammarCorrection.correctGrammar(input_text)
        self.assertIn("He doesn't have time", corrected_text)

    # testing edge cases
    def test_edge_case_nonsense_input(self):
        """Ensure the model doesn't crash on gibberish input."""
        input_text = "asdfghjkl"
        corrected_text = self.grammarCorrection.correctGrammar(input_text)
        self.assertIsInstance(corrected_text, str)

if __name__ == '__main__':
    unittest.main()

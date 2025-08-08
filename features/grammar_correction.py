from happytransformer import HappyTextToText, TTSettings
import nltk

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class GrammarCorrection:

    # constructor to initialize the model
    def __init__(self):
        self.happy_tt, self.args = self.loadModel()

    # load the language model for grammar correction
    def loadModel(self):
        """"Load the language model for grammar correction."""
        happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

        args = TTSettings(num_beams=5, min_length=1)

        return happy_tt, args

    # correct grammar in the given text
    def correctGrammar(self, text):
        """Correct grammar in the given text."""
        sentences = sent_tokenize(text)
        result = ""
        for s in sentences:
            corrected = self.happy_tt.generate_text(s, args=self.args)
            result += corrected.text + " "

        print(f"Corrected text: {result.strip()}")
        return result.strip()
        




from transformers import *
import librosa
import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

class SpeechToEmotion:
    def __init__(self):
        self.feature_extractor, self.model = self.loadModel()

    # Load the Wav2Vec2 model for emotion recognition
    def loadModel(self):
        """Load the Wav2Vec2 model for emotion recognition."""
        model_id = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
        feature_extractor = AutoFeatureExtractor.from_pretrained(model_id, do_normalize=True)
        model = AutoModelForAudioClassification.from_pretrained(model_id)
        return feature_extractor, model

    # Predict emotion from audio using Wav2Vec2
    def predictEmotion(self, audio_path):
        """Predict emotion from audio using Wav2Vec2."""
        audio, rate = librosa.load(audio_path, sr=16000)
        inputs = self.feature_extractor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            outputs = self.model(inputs.input_values)
            predictions = torch.nn.functional.softmax(outputs.logits.mean(dim=1), dim=-1)  # Average over sequence length
            predicted_label = torch.argmax(predictions, dim=-1)
            emotion = self.model.config.id2label[predicted_label.item()]
        return emotion
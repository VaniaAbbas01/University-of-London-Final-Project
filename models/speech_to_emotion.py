from transformers import *
import librosa
import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

def loadModel():
    model_id = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_id, do_normalize=True)
    model = AutoModelForAudioClassification.from_pretrained(model_id)
    return feature_extractor, model

def predictEmotion(audio_path):
    """Predict emotion from audio using Wav2Vec2."""
    feature_extractor, model = loadModel()
    audio, rate = librosa.load(audio_path, sr=16000)
    inputs = feature_extractor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = model(inputs.input_values)
        predictions = torch.nn.functional.softmax(outputs.logits.mean(dim=1), dim=-1)  # Average over sequence length
        predicted_label = torch.argmax(predictions, dim=-1)
        emotion = model.config.id2label[predicted_label.item()]
    return emotion

from transformers import *
import librosa
import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import numpy as np
import pandas as pd
import time
import csv
from tabulate import tabulate


# CSV path 
CSV_PATH = "./audioFiles/audio.csv"     

# Store results here
results = []


# model for speech-to-emotion recognition using Wav2Vec2
# feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")
# # model = Wav2Vec2ForCTC.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")
# model = AutoModelForAudioClassification.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")

model_id = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"

feature_extractor = AutoFeatureExtractor.from_pretrained(model_id, do_normalize=True)
model = AutoModelForAudioClassification.from_pretrained(model_id)



def predict_emotion(audio_path):
    audio, rate = librosa.load(audio_path, sr=16000)
    inputs = feature_extractor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = model(inputs.input_values)
        predictions = torch.nn.functional.softmax(outputs.logits.mean(dim=1), dim=-1)  # Average over sequence length
        predicted_label = torch.argmax(predictions, dim=-1)
        emotion = model.config.id2label[predicted_label.item()]
    return emotion


# read csv file
df = pd.read_csv(CSV_PATH)


print("Benchmarking Models...")
for i, row in df.iterrows():
    audio_file = row["filename"]
    reference = row["emotion"]

    start = time.time()
    result = predict_emotion("./audioFiles/" + audio_file)
    end = time.time()

    inference_time = round(end - start, 2)    

    results.append([
    "Wav2Vec2 (r-f)",
    audio_file, 
    inference_time,
    result, 
    reference
    ])

# Print table
print("\nTranscription Time Comparision:")
print(tabulate(results, headers=["Model", "Audio File", "Inference Time (s)", "Predicted Emotion", "Reference Emotion"]))

# Save to CSV
csv_path = "speech-to-emotion.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Model","Audio File", "Inference Time (s)", "Predicted Emotion", "Reference Emotion"])
    writer.writerows(results)

print(f"\nResults saved to: {csv_path}")

    
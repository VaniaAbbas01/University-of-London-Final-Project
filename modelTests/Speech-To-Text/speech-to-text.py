import time
import csv
import pandas as pd
from tabulate import tabulate
import whisper
from faster_whisper import WhisperModel
from jiwer import wer

# CSV path 
CSV_PATH = "./audioFiles/audio.csv"
# # Models to test
MODEL_SIZES = ["tiny", "base", "small"]

# # Store results here
results = []

df = pd.read_csv(CSV_PATH)
reference_text = []

for value in df["text"]:
    reference_text.append(value.strip().lower())

i = 0
for size in MODEL_SIZES:
    print("Benchmarking OpenAI Whisper...")
    sum_wer = 0
    for value in df['filename']:
        model = whisper.load_model(size)
        model.transcribe("./audioFiles/"+ value)
        start = time.time()
        result = model.transcribe("./audioFiles/"+ value) 
        duration = time.time() - start
        output_text = result["text"].strip().lower()
        error = wer(reference_text[i], output_text)
        sum_wer += error
    avg_wer = sum_wer / len(df['filename'])
    results.append([f"Whisper ({size})" ,f"{duration:.2f}",f"{avg_wer:.3f}"])
    if i <= len(reference_text) - 1:
        i = i + 1

i = 0

for size in MODEL_SIZES:
    sum_wer = 0
    for value in df['filename']:
        print("Benchmarking OpenAI Whisper...")
        model = WhisperModel(size, device="cpu", compute_type="int8")
        list(model.transcribe("./audioFiles/"+ value))

        start = time.time()
        segments, _ = model.transcribe("./audioFiles/"+ value)
        segments = list(segments)  
        duration = time.time() - start
        text = " ".join([seg.text for seg in segments])
        output_text = " ".join([seg.text for seg in segments]).strip().lower()
        print(output_text)
        error = wer(reference_text[i], output_text)
        sum_wer += error
    avg_wer = sum_wer / len(df['filename'])
    results.append([f"Faster-Whisper ({size})", f"{duration:.2f}", f"{avg_wer:.3f}"])
    if i <= len(reference_text) - 1:
        i = i + 1
        
# Print table
print("\nTranscription Time Comparison:")
print(tabulate(results, headers=["Model", "Inference Time (s)", "WER", "Word Error Rate"]))

# Save to CSV
csv_path = "speech-to-text.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Model", "Inference Time (s)", "WER"])
    writer.writerows(results)

print(f"\nResults saved to: {csv_path}")





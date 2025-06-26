import time
import csv
import pandas as pd
from tabulate import tabulate
from happytransformer import HappyTextToText, TTSettings
import language_tool_python

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

tool = language_tool_python.LanguageTool('en-US')

# CSV path 
CSV_PATH = "./grammar-correction.csv"

# Store results here
results = []

# read csv file
df = pd.read_csv(CSV_PATH)

# drop irrelevant columns
df = df.drop("Serial Number", axis=1) 

def count_errors(text):
    matches = tool.check(text)
    return len(matches)

reference_text = [value.strip().lower() for value in df["Standard English"]]

print("Benchmarking Grammar Correction Models...")
for i, row in df.iterrows():
    original_text = row["Ungrammatical Statement"].strip().lower()
    reference = row["Standard English"].strip().lower()

    result = happy_tt.generate_text(original_text, args=args)
    corrected = result.text.strip().lower()

    # Calculating Error Reduction Rate
    error_original = count_errors(original_text)
    error_corrected = count_errors(corrected)

    if error_original == 0:
        ERR = 0.0
    else:
        ERR = ((error_original - error_corrected) / error_original) * 100 

    # Calculating GLEU Score
    


# Print table
print("\nTranscription Time Comparison:")
print(tabulate(results, headers=["Model", "Inference Time (s)", "GLEU", "Sample Output", "Word Error Rate"]))

# # Save to CSV
# csv_path = "language-model.csv"
# with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Model", "Original Text", "Inference Time (s)", "WER", "Sample Output"])
#     writer.writerows(results)

# print(f"\nResults saved to: {csv_path}")





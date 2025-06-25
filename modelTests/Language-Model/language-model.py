import time
import csv
import pandas as pd
from tabulate import tabulate


# CSV path 
CSV_PATH = "./grammar-correction.csv"

# Store results here
results = []

# read csv file
df = pd.read_csv(CSV_PATH)

# drop irrelevant columns
df = df.drop("Serial Number", axis=1) 

reference_text = []

print(df.columns)

print(df.head())

# for value in df["Standard English"]:
#     reference_text.append(value.strip().lower())

# i = 0
# for value in df['filename']:
#     print("Benchmarking Grammar Correction Models...")
    
    
#     if i <= len(reference_text) - 1:
#         i = i + 1

# # Print table
# print("\nTranscription Time Comparison:")
# print(tabulate(results, headers=["Model", "Inference Time (s)", "GLEU", "Sample Output", "Word Error Rate"]))

# # Save to CSV
# csv_path = "speech-to-text.csv"
# with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Model", "Original Text", "Inference Time (s)", "WER", "Sample Output"])
#     writer.writerows(results)

# print(f"\nResults saved to: {csv_path}")





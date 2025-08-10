import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# function to plot bar charts
def plot(data, x_col, y_col, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_col], data[y_col], color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45) 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Attempt to read the CSV file
try:
    df = pd.read_csv("speech-to-text.csv")
except FileNotFoundError:
    print("CSV file not found. Please ensure the file exists in the current directory.")
    exit()

summary = df.groupby("Model").agg({
    "Inference Time (s)": "mean",
    "WER": "mean",
}).reset_index()

summary.columns = ["Model", "Mean Inference Time (s)", "Mean WER"]
print(summary)

# extracting mean of WER and Inference Time for each Model
mean_WER = summary[["Model", "Mean WER"]]
mean_IT = summary[["Model", "Mean Inference Time (s)"]]

# plotting the mean WER and Inference Time
plot(mean_WER, "Model", "Mean WER", "Mean WER by Model", "Model", "WER (%)")
plot(mean_IT, "Model", "Mean Inference Time (s)", "Mean Inference Time by Model", "Model", "Mean Inference Time (s)")










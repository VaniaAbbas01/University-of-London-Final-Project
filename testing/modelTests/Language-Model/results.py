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
    df = pd.read_csv("language-model.csv")
except FileNotFoundError:
    print("CSV file not found. Please ensure the file 'language-model.csv' exists in the current directory.")
    exit()

# Data preprocessing
df["Error Reduction Rate"] = df["Error Reduction Rate"].str.replace('%', '').astype(float)
df["GLEU"] = df["GLEU"].astype(float)
df[["Original_Errors", "Corrected_Errors"]] = df["Errors (Original → Errors Corrected)"].str.extract(r"(\d+) → (\d+)").astype(int)
df["Errors_Reduced"] = df["Original_Errors"] - df["Corrected_Errors"]

summary = df.groupby("Model").agg({
    "Inference Time (s)": "mean",
    "Error Reduction Rate": "mean",
    "GLEU": "mean",
    "Errors_Reduced": "sum"
}).reset_index()

summary.columns = ["Model", "Mean Inference Time (s)", "Mean Error Reduction Rate (%)", "Mean GLEU", "Total Errors Reduced"]
print(summary)

# calculating the mean of the inference time for each model
mean_inference_time = summary[["Model", "Mean Inference Time (s)"]]
# plotting the mean inference time
plot(mean_inference_time, "Model", "Mean Inference Time (s)", "Mean Inference Time by Model", "Model", "Inference Time (s)")

# calculating the mean of the Error Reduction Rate for each model
mean_ERR = summary[["Model", "Mean Error Reduction Rate (%)"]]
# plotting the mean Error Reduction Rate
plot(mean_ERR, "Model", "Mean Error Reduction Rate (%)", "Mean Error Reduction Rate by Model", "Model", "Error Reduction Rate (%)")

# calculating the mean of the GLEU for each model
mean_GLEU = summary[["Model", "Mean GLEU"]]
# plotting the mean GLEU
plot(mean_GLEU, "Model", "Mean GLEU", "Mean GLEU Score by Model", "Model", "GLEU Score")










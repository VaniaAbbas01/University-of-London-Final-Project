import time
import csv
import pandas as pd
from tabulate import tabulate
from happytransformer import HappyTextToText, TTSettings
from transformers import pipeline
import language_tool_python
import nltk
from nltk.translate.gleu_score import sentence_gleu
from nltk.tokenize import word_tokenize

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

corrector = pipeline(
              'text2text-generation',
              'pszemraj/grammar-synthesis-small',
              )

tool = language_tool_python.LanguageTool('en-US')
nltk.download('punkt_tab')

# CSV path 
CSV_PATH = "./grammar-correction.csv"

# Store results here
results = []

# read csv file
df = pd.read_csv(CSV_PATH)

# drop irrelevant columns
df = df.drop("Serial Number", axis=1) 

# samples per category
n_samples = 10

df = df.groupby('Error Type').apply(lambda x: x.sample(n=min(len(x), n_samples), random_state=42))

df.reset_index(drop=True, inplace=True)

def count_grammar_errors(text, verbose=False):
    matches = tool.check(text)
    grammar_errors = [
        m for m in matches 
        if not m.ruleId.startswith("UPPERCASE") and
           not m.ruleId.startswith("EN_QUOTES") and
           not m.ruleId.startswith("PUNCTUATION") and
           not m.ruleId.startswith("WHITESPACE") and
           not m.ruleId.startswith("MORFOLOGIK_RULE_EN_US")  # Spelling
    ]
    if verbose:
        for m in grammar_errors:
            print(f"[{text}] → {m.ruleId} ({m.message})")
    return len(grammar_errors)

reference_text = [value.strip().lower() for value in df["Standard English"]]

print("Benchmarking Grammar Correction Models...")
for i, row in df.iterrows():
    original_text = row["Ungrammatical Statement"].strip().lower()
    reference = row["Standard English"].strip().lower()

    start = time.time()
    result = happy_tt.generate_text(original_text, args=args)
    end = time.time()

    corrected = result.text.strip().lower()
    inference_time = round(end - start, 2)    

    # Calculating Error Reduction Rate
    error_original = count_grammar_errors(original_text, verbose=True)
    error_corrected = count_grammar_errors(corrected, verbose=True)

    # Calculating GLEU Score
    ref_tokens = [word_tokenize(reference)]
    hyp_tokens = word_tokenize(corrected)    
    gleu = sentence_gleu(ref_tokens, hyp_tokens)

    if error_original == 0:
        ERR = 0.0
    else:
        ERR = ((error_original - error_corrected) / error_original) * 100 

    results.append([
    "T5 (vennify)", 
    original_text,
    inference_time,
    f"{ERR:.2f}%", 
    f"{gleu:.3f}", 
    f"{error_original} → {error_corrected}"
    ])
    
for i, row in df.iterrows():
    original_text = row["Ungrammatical Statement"].strip().lower()
    reference = row["Standard English"].strip().lower()

    start = time.time()
    result = corrector(original_text)
    end = time.time()

    corrected = result[0]["generated_text"].strip().lower()
    inference_time = round(end - start, 2)    

    # Calculating Error Reduction Rate
    error_original = count_grammar_errors(original_text, verbose=True)
    error_corrected = count_grammar_errors(corrected, verbose=True)

    # Calculating GLEU Score
    ref_tokens = [word_tokenize(reference)] 
    hyp_tokens = word_tokenize(corrected)
    gleu = sentence_gleu(ref_tokens, hyp_tokens)

    if error_original == 0:
        ERR = 0.0
    else:
        ERR = ((error_original - error_corrected) / error_original) * 100 

    results.append([
    "FLAN T5 (pszemraj)", 
    original_text,
    inference_time,
    f"{ERR:.2f}%", 
    f"{gleu:.3f}", 
    f"{error_original} → {error_corrected}"
    ])

# Print table
print("\nTranscription Time Comparison:")
print(tabulate(results, headers=["Model", "Original Text", "Inference Time (s)", "Error Reduction Rate", "GLEU", "Errors (Original ➜ Errors Corrected)"]))

# Save to CSV
csv_path = "language-model.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Model", "Original Text", "Inference Time (s)", "Error Reduction Rate", "GLEU", "Errors (Original → Errors Corrected)"])
    writer.writerows(results)

print(f"\nResults saved to: {csv_path}")
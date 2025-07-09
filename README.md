# University-of-London-Final-Project

## Folder structure

Final Year Project/
|
├── modelTests/
│ ├──Speech-To-Text
│ | ├── speech-to-text.py
│ | └── audioFiles
│ | ├── speech-to-text.py
│ | └── csv data
| ├──Language-Model
│ ├── language-model.py
│ └── grammar-correction.csv
│ ├── results.py
│ └── language-model.csv
├── templates/
│ ├── index.html
│ ├── feedback.html
│ └── video.html
├── main.py
|

## Setup Requirements

### User Interface

The following package is required to run the web application:

- [`Flask`](https://pypi.org/project/Flask/) – lightweight web framework for Python

### Benchmarking Packages

#### Speech To Text Models

- `time` – Standard Python module for tracking execution time
- `csv` – Standard module to read/write CSV files
- `pandas` – For data manipulation and analysis
- `tabulate` – To print tabular results in a readable format
- `whisper` – OpenAI's Whisper ASR model
- `faster-whisper` – Optimized Whisper implementation for faster inference
- `jiwer` – Measures Word Error Rate (WER) for accuracy evaluation

#### Language Models

These packages support text generation, grammar correction, and benchmarking:

- `time` – Execution time measurement
- `csv` – File I/O
- `pandas` – Data handling
- `tabulate` – Output formatting
- `happytransformer` – Simplified interface to use NLP models
- `transformers` – Hugging Face’s NLP model library
- `nltk` – Tokenization, BLEU/GLEU scoring, etc.
- `language_tool_python` – Grammar and spelling correction tool

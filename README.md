# University-of-London-Final-Project

## Folder Structure

```bash
Final-Year-Project/
│
├── features/ # Core functionality and ML models
│   ├── audio_analysis.py # Extracts acoustic features (pitch, intensity, jitter, etc.)
│   ├── grammar_correction.py # Grammar correction using pretrained LM
│   ├── language_analysis.py # Fluency, vocabulary richness, filler word detection
│   ├── speech_to_emotion.py # Emotion classification from audio
│   └── speech_to_text.py # Speech-to-text transcription
│
├── routes/ # Flask route handlers
│   ├── analysisRoute.py # Handles /analyse (feedback generation)
│   ├── mainRoute.py # Handles main index page
│   └── uploadRoute.py # Handles audio upload & transcription
│
├── services/ # Helper services
│   ├── audioService.py # File validation, audio duration
│   └── feedbackService.py # Orchestrates feedback generation
│
├── static/ # Static files (CSS, JS, images)
│   ├──  styles.css
│   └── script.js
│
├── templates/ # Frontend templates (Jinja2 + HTML)
│   ├── index.html
│   ├── feedback.html
│   └── transcription.html
│
├── tests/ # Testing modules
│   ├── model-tests/ # Model benchmarking & evaluation
│   └── unit-tests/ # Unit and functional tests
│
├── config.py # App configuration
├── main.py # Entry point (Flask app launcher)
├── requirements.txt # Python dependencies
└── README.md
```

---

## Setup Requirements

### User Interface

- [Flask](https://pypi.org/project/Flask/) – lightweight web framework for Python
- Other dependencies (ML/NLP/audio packages) are listed in **`requirements.txt`**

### Audio File Processing

- [ffmpeg](https://www.ffmpeg.org/download.html) - Whisper model requires `ffmpeg` software to process audio files for transcription

---

## Running the Application

This system uses Python `3.10.11`

### 1. Create virtual environment

On Windows:

`python -m venv venv`

On Linux/macOS:

`python3 -m venv venv`

### 2. Activate virtual environment

On windows:

`venv\Scripts\activate`

On Linux/macOS:

`source venv/bin/activate`

### 3. Install dependencies

`pip install -r requirements.txt`

### 4. Run the Flask app:

`python main.py`

### 5. Open your browser at:

`http://127.0.0.1:5000/`

---

## Running Tests

### Unit Tests

From the root of the folder, use command:

- run `python -m unittest tests.unit-tests.<filename.py>`

### Model Tests

- "cd" into **tests/model-tests** folder from folder root
- "cd" into a specific folder for the benchmark scripts you want to run
- run `python <filename.py>`

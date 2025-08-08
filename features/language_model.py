import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}  # Replace with your actual token

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)
    response.raise_for_status()
    return response.json()

# Example speech features
speech_features = {
    "clarity_score": 6.5,
    "filler_words": 12,
    "speaking_rate": 140,
    "emotion": "nervous",
    "pronunciation": "average"
}

prompt = f"""[INST]
You are a speech coach. Based on the following features, provide clear, constructive, and encouraging feedback to the speaker. Keep the tone supportive and concise.

Clarity Score: {speech_features['clarity_score']}
Filler Words: {speech_features['filler_words']}
Speaking Rate: {speech_features['speaking_rate']} words per minute
Emotion Detected: {speech_features['emotion']}
Pronunciation: {speech_features['pronunciation']}

Provide your feedback in less than 100 words.
[/INST]"""

output = query({
    "inputs": prompt,
    "parameters": {
        "return_full_text": False,
        "max_new_tokens": 150
    }
})

print(output[0]["generated_text"])

"""
feedback = {
        "transcription": corrected_text,
        "fluency": {
            "words_per_minute": 20,
            "filler_words": 20,
            "pauses": 0 
        },
        "tone":confident,
        "feedback": [
            {"type": "Pacing", "suggestion": "Your pace is good. Keep it up!"},
            {"type": "Grammar", "suggestion": "Minor sentence structure improvements made."},
            {"type": "Filler Words", "suggestion": "Good job! You used very few filler words. Try to stay mindful to reduce them further."},
        ]
    }
"""

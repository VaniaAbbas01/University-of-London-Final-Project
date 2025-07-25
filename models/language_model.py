from transformers import T5Tokenizer, T5ForConditionalGeneration
import json

def loadModel():

    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    return tokenizer, model

def prompt(feedback):
    tokeniser, model = loadModel()

    input_text = f"""Given this feedback JSON: {json.dumps(feedback, indent=2)},
    summarize it and give the user specific suggestions for improvement."""
    
    input_ids = tokeniser(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids)
    print(tokeniser.decode(outputs[0]))
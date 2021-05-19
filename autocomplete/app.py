from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import math
import re
from transformers import pipeline, set_seed

# Loading the model
print("Loading the model..........")
model = pipeline('text-generation', model='gpt2')

app = Flask(__name__)

@app.route('/autocomplete',methods=['POST'])
def generate():
    '''
        To use the context and return a list of 3 sentences that contains the next 10 words after context for autocomplete
    '''
    data = request.get_json(force=True)
    context = data['context']
    num_of_tokens = data['num_of_tokens']
    print(num_of_tokens)
    # Initializing the result dictionary
    final_result = {"generated_text_list":[],"error":""}
    try:
        # Using the model to generate next 3 sequences
        result = model(context, max_length=len(context.split())+int(num_of_tokens), num_return_sequences=3, return_full_text=False)
        result_list = [item["generated_text"].replace("\n"," ").replace("\\","") for item in result]
        final_result["generated_text_list"] = result_list
    except Exception as error: 
        # Get the error message in the result 
        final_result["error"] = str(error)
        
    return jsonify(final_result)

if __name__ == '__main__':
    app.run(port=4000, debug=True)

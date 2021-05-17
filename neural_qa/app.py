from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import math
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering

# Loading the model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")
model = TFAutoModelForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad", return_dict=True)

app = Flask(__name__)

@app.route('/answer',methods=['POST'])
def process():
    '''
        To process the text and return the answer with highest score. 
        The function breaks the text into segments of 450 tokens, calls answer function on each and returns the answer
        with highest score
    '''
    data = request.get_json(force=True)
    text = data['text']
    query = data['query']

    # Initializing the result dictionary
    final_result = {"answer":"","score":-100,"error":""}
    try:
        length = len(text)
        text_list = []
        result_dict={}
        if length>450:
            no_of_segments = math.ceil(length/400)
            for i in range(no_of_segments):
                segment = str(text[(i*400):(i*400)+450])
                result = answer(query, segment)
                result_dict[result['answer']] = result['score']
            result_dict = sorted(result_dict.items(),key=lambda item:item[1],reverse=True)
            final_result["answer"] = result_dict[0][0]
            final_result["score"] = result_dict[0][1]
        else:
            final_result = answer(query, text) 
            
    except Exception as error: 
        # Get the error message in the result 
        final_result["error"] = str(error)
        
    return jsonify(final_result)
    
def answer(query, text):
    '''
        This function computers the answer and it's score given a query and context text
    '''
    inputs = tokenizer(query, text, add_special_tokens=True, return_tensors="tf")
    input_ids = inputs["input_ids"].numpy()[0]
    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    output = model(inputs)

    start_logits = output.start_logits[0].numpy()
    end_logits = output.end_logits[0].numpy()

    answer_start = tf.argmax(output.start_logits, axis=1).numpy()[0]  # Get the most likely beginning of answer with the argmax of the score
    answer_end = (tf.argmax(output.end_logits, axis=1) + 1).numpy()[0]  # Get the most likely end of answer with the argmax of the score 

    score = start_logits[answer_start] + end_logits[answer_end-1] # Get the score of answers

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    return {'answer':answer, 'score': round(score)}


if __name__ == '__main__':
    app.run(port=5000, debug=True)

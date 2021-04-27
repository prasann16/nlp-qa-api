from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering

# Loading the model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = TFAutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad", return_dict=True)

app = Flask(__name__)

@app.route('/answer',methods=['POST'])
def answer():
    try: 
        data = request.get_json(force=True)
        text = data['text']
        question = data['query']

        inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="tf")
        input_ids = inputs["input_ids"].numpy()[0]
        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        output = model(inputs)

        start_logits = output.start_logits[0].numpy()
        end_logits = output.end_logits[0].numpy()

        answer_start = tf.argmax(output.start_logits, axis=1).numpy()[0]  # Get the most likely beginning of answer with the argmax of the score
        answer_end = (tf.argmax(output.end_logits, axis=1) + 1).numpy()[0]  # Get the most likely end of answer with the argmax of the score 

        score = start_logits[answer_start] + end_logits[answer_end-1] # Get the score of answers

        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    
    except Exception as error: 
        print(error)
        answer = ""
        score = -100

    return jsonify({'answer':answer, 'score': str(score)})
    # return jsonify({'result':'BLOOR ST E and TED ROGERS WAY'})


if __name__ == '__main__':
    app.run(port=5000, debug=True)

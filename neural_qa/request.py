import json
import requests

def api_request(url, json_data):
    print(json_data)
    r = requests.post(url,json=json_data)
    return r.json()

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

if __name__ == '__main__':

    # API_URL = "https://api-inference.huggingface.co/models/gpt2"
    # headers = {"Authorization": f"Bearer api_CeWVOOMYZrgWCiMUKxnOYjqgUoCqgdJYbb"}

    # data = query({"inputs": "What is the speed of a train"})
    # print(data)
    text = "JSON is a format for serialising object data. It doesn't really care or know about Python types, the json package tries to translate whatever object you pass json.dumps() into a string form via a conversion table that only supports some types (see doc below)."
    query = "What is JSON?"
    print(f"Text: {text}\n")
    print(f"Query: {query}\n")    
    result = api_request('http://localhost:5000/answer', {'text':text, 'query': query})
    print(result)

import requests
import json
def api_request(url, json_data):
    r = requests.post(url,json=json_data)
    return r.json()

if __name__ == '__main__':
    # Example of the autocomplete API request
    context = "What is the speed of Boeing"
    num_of_tokens = 10 # The number of next words to be returned
    data = {'context':context,'num_of_tokens':num_of_tokens}
    result = api_request('http://localhost:4000/autocomplete', json_data=data)
    print(result["generated_text_list"])
import requests
import json
def api_request(url, json_data):
    r = requests.post(url,json=json_data)
    return r.json()

if __name__ == '__main__':
    result = api_request('http://localhost:4000/autocomplete', {'context':"What is the speed of Boeing",'num_of_tokens':5})
    print(result)
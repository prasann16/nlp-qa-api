# bold-stratus-nlp
NLP APIs for Bold Stratus

This project uses `Python based Flask framework` for the API

1. **To get started with running the code, first install** `Conda` **Package manager. This is a python package manager which makes it easy to create python environments and install libraries.**
To install conda, go here: https://docs.conda.io/projects/conda/en/latest/user-guide/install/

2. **Create a python environment**
To create a python environment using conda, open your Terminal or Command Prompt and run this command:
`conda create -n bold-stratus python=3.7`
This will create a python environment named `bold-stratus`

3. **Now, pull the latest code from** `master` **branch on this repo. 

4. **Get into the newly created environment using** `conda activate bold-stratus`.

5. **Install required libraries using** `pip install -r requirements.txt`. **This will install all the required libraries for this project.**

6. **Now you can run the server using:** `python app.py`

8. **The API will run on `port 5000`. 


# File descriptions
- `app.py` - Main server file
- `requests.py` - Example api request for testing
- `requirements.py` - All required libraries for this project

# Question Answering API
- The question answering API uses `distilbert-base-uncased-distilled-squad` model from https://huggingface.co. 

**Query**: 
{'text':"JSON is a format for serialising object data", 'query': "What is JSON?"}
- Both the "text" and "query" need to be in string format

**Result**: 
{'answer': 'a format for serialising object data', 'score': '18.858807'}

- The api will return an answer with a score. This score is not from 0-100. It will range from -20 to +30. 
- The score will be in string format so you will need to convert it to `int` or `float` to set a threshold after receiving the result. 
- From preliminary testing, anything over score of 10 means a good result. 

**Error**:
- In case of error in the application, the answer will be "" (empty string) and the score will be -100. 

For questions about this, please email prasannpandya1@gmail.com



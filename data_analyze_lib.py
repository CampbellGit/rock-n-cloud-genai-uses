import json
from json import JSONDecodeError
from langchain_community.chat_models import BedrockChat

#

def get_llm():

    llm = BedrockChat( #create a Bedrock llm client
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs = {"temperature": 0.0 } #for data extraction, minimum temperature is best
    )

    return llm

#

def validate_and_return_json(response_text):
    try:
        response_json = json.loads(response_text) #attempt to load text into JSON
        return False, response_json, None #returns has_error, response_content, err 
    
    except JSONDecodeError as err:
        return True, response_text, err #returns has_error, response_content, err 

#

def get_json_response(input_content): #text-to-text client function
    
    llm = get_llm()

    response = llm.invoke(input_content) #the text response for the prompt
    
    return validate_and_return_json(response.content)
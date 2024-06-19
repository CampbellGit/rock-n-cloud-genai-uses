import boto3
import json
import base64
from io import BytesIO
import vertexai
from vertexai.generative_models import GenerativeModel, Content, Part, FinishReason
import vertexai.preview.generative_models as generative_models


#get a BytesIO object from file bytes
def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io


#get a base64-encoded string from file bytes
def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


#generate a response using Anthropic Claude
def get_response_from_model(prompt_content, image_bytes, mask_prompt=None):
    generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
        
    vertexai.init(project="daveo-gcp-gemini-sbx-8895", location="europe-west9")
    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )

    image_vertex = Part.from_data(
        mime_type="image/jpeg",
        data=get_base64_from_bytes(image_bytes))

    responses = model.generate_content(
        [image_vertex, prompt_content],  # Pass Content objects here
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    gemini_output=""

    for response in responses:
        print(response.text)
        gemini_output+=response.text
    
    return gemini_output
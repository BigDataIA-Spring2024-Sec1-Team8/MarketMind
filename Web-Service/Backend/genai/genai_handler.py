import google.generativeai as genai
from openai import OpenAI
import os
genai.configure(api_key=os.getenv('gemini_key'))

client = OpenAI(api_key=os.getenv('openai_key'))


def call_gemini_api(input_text):
    model = genai.GenerativeModel('models/gemini-1.0-pro')
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages = [
    #         {
    #         "role": "user",
    #         "content": input_text
    #         }]
    # )

    # return response.choices[0].message.content
    response = model.generate_content(input_text.strip(), safety_settings={'HARASSMENT':'block_none',
                                                     'HATE_SPEECH': 'block_none',
                                                     'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
                                                     'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none'})
    try:
        return response.text
    except Exception as e:
        # print(response.prompt_feedback)
        return "what products are you looking for ?"
    
def call_openai_api(input_text):
    # model = genai.GenerativeModel('models/gemini-1.0-pro')
    

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [
                {
                "role": "user",
                "content": input_text
                }]
        )

        return response.choices[0].message.content
    except Exception as e:
        # print(response.prompt_feedback)
        return "what products are you looking for ?"
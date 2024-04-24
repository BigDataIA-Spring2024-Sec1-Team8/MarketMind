from genai.genai_handler import call_gemini_api
import re
import json
def find_followup_or_not(messages):
    condensed_prompt = ""
    for msg in messages:
        if msg.role == 'user':
            condensed_prompt += f"User: {msg.content}\n"
        # else:
        #     condensed_prompt += f"Assistant: {msg.content}\n"
    print(condensed_prompt)
    prompt = f"""
    Decide whether to fetch products and determine if a clarifying question is needed

    Inputs:
    - chat_history: {condensed_prompt}
    """+"""
    Instructions:
    1. If the latest message refers to selecting products from previously asked product for any use case or activity, output "No" for fetch_products.
    2. If the latest message in chat_history is the user's first question about a product, output "Yes" for fetch_products.
    3. Otherwise:
        b. If there are no previous questions about a product that the user is referring to in the latest message, output "Yes" for fetch_products.
    4. Check if you can fetch what category user is refering to from chat_history.
        ['men_clothing', 'women_clothing', 'men_watches','women_watches', 'men_shoes', 'women_shoes']
    Examples to say no for fetching products:
    - which one suit for part?
    - which one matches activity?
    Output:
    A JSON object with the following keys:
    - "fetch_products": A string "Yes" or "No" indicating whether
 to fetch products or not.
    - "question_to_ask": A clarifying question for the user, or "
null" if no question is needed.
    - explanation: "why yes/no for fetch products in your respons
e",
    Format:
    {
        "fetch_products": "No",
        "explanation": "why yes/no for fetch products in your res
ponse",
        "question_to_ask": question to ask user/null
    }
    """
    response = call_gemini_api(prompt)
    res = {
        "fetch_products": "Yes",
        "question_to_ask": None
    }
    try:
        start_index = response.index('{')
        end_index = response.rindex('}')
        res = json.loads(response[start_index:end_index+1])
    except Exception as e:
        print(str(e))
    
    return res
def condense_messages(messages, gender = "men"):
    """
    Function to condense the last 4 messages into a prompt.
    """
    condensed_prompt = "Previous messages:\n"
    for msg in messages:
        if msg.role == 'user':
            condensed_prompt += f"User: {msg.content}\n"
        # else:
        #     condensed_prompt += f"Assistant: {msg.content}\n"
    newp = f"""
    Identify products, descriptions, and categories from the user's latest message.
      Use chat history only if user is refering to previous products
    
    "Users gender is {gender}"
    
    Inputs:
    - chat_history: {condensed_prompt}
    """+"""
    Instructions:
    1. Identify the products the user is referring to in the late
st_message.
    2. For each identified product:
        a. If the user provides enough details to describe the pr
oduct, summarise those details as the "description".
        b. If the user does not provide enough details, use the p
roduct name itself as the "description".
    4. Classify each product into one of the following categories
:
        ['men_clothing', 'women_clothing', 'men_watches', 'women_
watches', 'men_shoes', 'women_shoes']

    CONSTRAINTS:

    Use only the products referenced in the latest_message. Ignor
e all other products.

    ALL THE PRODUCTS SHOULD BE FROM SAME GENDER [MEN/WOMEN]. DONT
 MIX THEM

    Output:
    A JSON object with a list of product objects, each containing
 "name", "description", and "category" keys.
    Format and example:
    {
        "products": [
            {
                "name": "blue jeans",
                "description": "blue denim jeans",
                "category": "men_clothing"
            },
            {
                "name": "white shirts",
                "description": "white shirts",
                "category": "women_clothing"
            }
        ]
    }
    """


    response = call_gemini_api(newp)
    print(response, "imp")
    res = {
        "products": [
        ]
    }
# Extracting multiple products and their descriptions
    try:
        start_index = response.index('{')
        end_index = response.rindex('}')
        print(response[start_index:end_index+1])
        res = json.loads(response[start_index:end_index+1])
    except Exception as e:
        print(str(e))
    # Iterating through lines to extract product information
    
    return res
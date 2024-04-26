from genai.genai_handler import  call_openai_api
import re
import json

def pick_products(message, gender = "men"):
    """
    Function to condense the last 4 messages into a prompt.
    """
    # condensed_prompt = "Previous messages:\n"
    # for msg in messages:
    #     if msg.role == 'user':
    #         condensed_prompt += f"User: {msg.content}\n"
        # else:
        #     condensed_prompt += f"Assistant: {msg.content}\n"
    newp = f"""
    You are a fashion designer who helps to identify products, descriptions, and categories that should be served for user.

    "Users gender is {gender}"
    
    Inputs:
    - User Query: {message}
    """+"""
    Instructions:
    1. Identify all the products or series of products to serve best to the user is referring.
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

    ALL THE PRODUCTS SHOULD BE FROM SAME GENDER [MEN/WOMEN]. DONT MIX THEM

    Output:

    A JSON object with a list of product objects, each containing "name", "description", and "category" keys.
    
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
    print(newp)

    response = call_openai_api(newp)
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
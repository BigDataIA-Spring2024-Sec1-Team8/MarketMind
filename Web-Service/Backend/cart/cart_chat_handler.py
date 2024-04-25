from helpers.helper_functions import is_greeting
from prompt.prompt_handler import create_user_query_answering_cart
from genai.genai_handler import call_gemini_api
import json
def answer_questions_for_cart(cartReq):
    messages = cartReq.messages
    ref_products = cartReq.products
    response = {
        "bot":  "Hello! How can I assist you today?",
        "products": []
    }
    if is_greeting(messages[-1].content):
        response['bot'] = "Hello! How can I assist you today?"
        response['products'] = []
    else:
        product_details = ""
        for product in ref_products:
            product_details+=f"title: {product.title}"
            product_details+= f"description: {product.summary}"
            product_details+= f"asin: {product.asin}"
        prompt = create_user_query_answering_cart(message=messages[-1].content, product_info=product_details)
        print(prompt)
        response_message = call_gemini_api(prompt)
        try:
            response = {}
            start_index = response_message.index('{')
            end_index = response_message.rindex('}')
            print(response_message[start_index:end_index+1])
            res = json.loads(response_message[start_index:end_index+1])
            targets = res['products']
            response['bot'] = res['message']
            response['products'] = list(filter(lambda x: x.asin in targets,ref_products))
        except Exception as e:
            print(str(e))
    return {"response": response}
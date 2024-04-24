from chat.image_query_handler import handle_image
from prompt.prompt_handler import  create_sales_prompt_existing_products, create_sales_prompt
from helpers.helper_functions import is_greeting
from chat.chat_helper_functions import condense_messages,find_followup_or_not
from snowflake.snowflake_wrapper import insert_user_searches, get_product_data
from genai.embedding_handler import retrieve_products
from genai.genai_handler import call_gemini_api
from collections import defaultdict
from snowflake.snowflake_wrapper import retrieve_user_gender
def answer_user_query_bot(req):
    messages = req.messages
    ref_products = req.products
    gender = retrieve_user_gender(user_id=req.user_id)
    prompt = ""   
    if req.image != "":
        image_query = handle_image(req.image, messages[-1].content)
        messages[-1].content = image_query['query'] if 'query' in image_query else messages[-1].content

    res = find_followup_or_not(messages)
    # res = condense_messages(messages)
    fetch_more_products = res['fetch_products']
    question_to_ask = res['question_to_ask']
    response = {}

    if is_greeting(messages[-1].content):
        response['bot'] = "Hello! How can I assist you today?"
        response['products'] = []
        response['queries'] = {}
    elif question_to_ask and question_to_ask!= 'null':
        response['bot'] = question_to_ask
        response['products'] = []
        response['queries'] = {}

    elif len(messages) ==1 or fetch_more_products == 'Yes':
        all_products = []
        res_cond = condense_messages(messages, gender=gender)
        response['products']= defaultdict(list)
        response['queries']= defaultdict(str)
        products_descriptions = []
        user_searches = []
        for line in res_cond['products']:
            current_product = {}
            current_product["name"] = line['name']
            current_product["description"] = line['description'] 
            user_searches.append(current_product['description'])
            current_product["category"] = line['category']
            products_descriptions.append(current_product)
        insert_user_searches(req.user_id, user_searches)
        for p in products_descriptions:
            products = retrieve_products(prompt=p['description'] + " " + p['name'] if p['description'] else p['name'], category=p['category'])
            products_data = get_product_data(products)
            response['products'][p['name']] = products_data
            response['queries'][p['name']] = p['description'] + " "+ p['name'] if p['description'] else p['name']
            all_products.extend(products_data)

        sales_prompt = create_sales_prompt(prompt, all_products)
        response['bot'] = call_gemini_api(sales_prompt)
    else:
        response['products']= ref_products
        products_descriptions = []
        combine_lists = lambda d: [x for v in d.values() for x in (v if isinstance(v, list) else [])]
        combined_pro = combine_lists(ref_products)
        
        sales_prompt = create_sales_prompt_existing_products(messages[-1].content, combined_pro)
        response['bot'] = call_gemini_api(sales_prompt)

        # response['bot'] = "bot should use same questions to answer follow-up"
        response['products'] = ref_products
        response['queries'] = {}

    return {"response": response}

def show_more_products(req):
    cat = req.category.lower().replace(' ', '_') if req.category else "men_clothing"
    products = retrieve_products(prompt=req.query, category=cat,k=10)
    products = products[5:] if len(products) >5 else products
    products_data = get_product_data(products)
    response = {}
    response['products'] = products_data
    return {"response": response}
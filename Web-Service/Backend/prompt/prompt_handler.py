def create_sales_prompt(message, product_info):
    """
    Function to create a prompt for selling the products.
    """
    sales_prompt = f"Based on the user's message: '{message}', provide a persuasive and engaging response in not more than line to sell the following products:\n\n"
    for product in product_info:
        sales_prompt += f"Product: {product['title']}\nDescription: {product['summary']}\n\n"
    sales_prompt += "Response:"
    return sales_prompt


def create_sales_prompt_existing_products(message, product_info):
    """
    Function to create a prompt for selling the products.
    """
    sales_prompt = f"Based on the user's message: '{message}', provide a persuasive and engaging response in not more than line to answer user question. If user asks to pick one product for them, pick product based on description and convince user that the product is best for their query\n\n"
    for product in product_info:
        sales_prompt += f"Product: {product.title}\nDescription: {product.summary}\n\n"
    sales_prompt += "Response:"
    return sales_prompt

def create_user_query_answering_cart(message, product_info):
    """
    Function to create a prompt for selling the products.
    """
    sales_prompt = f"Based on the following product details: '{product_info}', \n\nAnswer User's query {message}"
    sales_prompt += """
    You are fashion designed recommending styles to user. If you user asks you to select outfit or justify outfit answer based on product descriptions
    If you don't find context which product suits other, use general knowledge. Don't say you dont know. 
    Return only products that answers user query.
    Pick products you are refering to answer user query in below format:
    {
    "message": "response",
    "products": [asin1,asin2, asin3]
    }
    """
    return sales_prompt
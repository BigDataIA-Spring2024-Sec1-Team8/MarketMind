from image_search.image_embedding import generate_image_embedding, retrieve_products

from PIL import Image
from openai import OpenAI
import base64
import os
import json
from snowflake.snowflake_wrapper import get_product_data

def resize_image(image_path, output_size):
    try:
        img = Image.open(image_path)
        img_resized = img.resize(output_size)
        img_resized.save(image_path)
        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False
client = OpenAI(api_key=os.getenv('openai_key'))

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

instruction = """
Ignore the person you are seeing in image, describe only the product that user is talking about. 
The product could be clothing, watches and shoes. 
You can consider gender of person to identify category from:
['men_clothing', 'women_clothing', 'men_shoes','women_shoes']
Give your answer in below format:\n
{
    "category": "one of categories given",
}
"""

def handle_image(file_path):   
    resize_image(file_path, (224, 224))
    base64_image = encode_image(file_path)
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages = [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": instruction
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ]
    )
    
    return response.choices[0].message.content
def retrieve_products_by_image(file):
    embedding = generate_image_embedding(file, '')
    response = handle_image(file)
    print(embedding, file)
    try:
       start_index = response.index('{')
       end_index = response.rindex('}')
       response = json.loads(response[start_index:end_index+1])
       category = response['category']
       print(category, embedding)
       products = retrieve_products(embedding.tolist()[0], category = category)
       print(products)
       products_data = get_product_data(products)
       return {"response": products_data}
    except Exception as e:
       print(str(e),"except")
    return {"response": []}


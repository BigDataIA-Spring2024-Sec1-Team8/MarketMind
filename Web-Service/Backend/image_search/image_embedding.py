from PIL import Image
import requests

from transformers import CLIPProcessor, CLIPModel
from pinecone import Pinecone
import os
pc = Pinecone(
        api_key=os.getenv('pinecone_key')
    )

def generate_image_embedding(url, summary_text):
    
    cache_dir = '.'
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32",cache_dir=cache_dir)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32",cache_dir=cache_dir)
    image = Image.open(url)

    inputs = processor(text=[summary_text], images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)    
    return outputs.image_embeds

def retrieve_products(embedding,category,k=5):
    """
    Function to retrieve relevant product information from Pinecone.
    """

    index = pc.Index('marketplace-images')
    results = index.query(vector=embedding, top_k=k,
                               namespace=category, include_values=True,
                               include_metadata=True
                               )
    products = [{"asin" : result['metadata']['asin']} for result in results['matches']]
    print(products)
    return products
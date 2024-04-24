import streamlit as st
import requests
import ast
from chat.message.images import image_interface

# Function to generate consistent-sized images in a horizontal scroll
def image_interface(image_urls):
    image_urls = ast.literal_eval(image_urls)
    images_html = " ".join(
        f'<img src="{url}" style="width:150px; height:150px; object-fit: cover; margin-right: 10px;" />'
        for url in image_urls
    )
    return f"<div style='overflow-x: auto; white-space: nowrap;'>{images_html}</div>"

# Function to search for products using an uploaded image
def search_image():
    st.markdown("<h2 style='color: #333;'>Search similar products or paired products with an Image 📷</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Search with an image...")

    if uploaded_file is not None:
        # Send the image to the FastAPI endpoint
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('http://chat-be-service:8000/search-image/', files=files)
        products = response.json()['response'] if 'response' in response.json() else []

        if response.status_code == 200:
            # Display each product in a card layout
            for product in products:
                image_html = image_interface(product['imageURLHighRes'])
                
                card_content = (
                    f"<div class='product-card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 15px 0; background-color: #f9f9f9;'>"
                    f"  <div style='text-align: center;'>"
                    f"    {image_html}"  # Embed consistent-sized images within card
                    f"  </div>"
                    f"  <div style='margin-top: 10px;'>"
                    f"    <h3 style='color: #333; font-weight: bold;'>{product['title']}</h3>"  # Product title with bold font
                    f"    <p style='color: #555; font-size: 14px; line-height: 1.5;'>{product['summary']}</p>"  # Product summary with consistent style
                    f"    <p style='color: #888; font-size: 12px; font-style: italic;'>ASIN: {product['asin']}</p>"  # ASIN with smaller font
                    f"  </div>"
                    f"</div>"
                )
                
                st.markdown(card_content, unsafe_allow_html=True)
        else:
            st.error(f'Error uploading image: {response.text}')

import streamlit as st
import ast
import requests
import base64
from uuid import uuid4
import json
from upload_to_s3 import upload_to_s3
from chat.message.images import image_interface
from gtts import gTTS
from io import BytesIO
# Function to prepare messages
def prepare_messages(new_message):
    messages = []
    if 'chat_history' in st.session_state:
        messages = st.session_state.chat_history[-4:]
    messages.append({"role": "user", "content": new_message})
    return messages

# Function to send a message
def send_message(messages, products, uploaded_file):
    url = "http://chat-be-service:8000/send/"
    s3_uri = ""
    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getvalue())
        s3_uri = upload_to_s3(uploaded_file.name, uploaded_file.name)
    json_req = {
        "user_id": st.session_state.get('user_id', 1),
        "messages": messages,
        "products": products,
        "image": f"{s3_uri}" if s3_uri != "" else s3_uri
    }
    
    response = requests.post(url, json=json_req)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        st.write(f"Please try again later")

# Function to add a product to the wishlist
def add_wishlist(product_id):
    url = "http://chat-be-service:8000/add-cart/"
    json_req = {
        "userid": st.session_state.get('user_id', 1),
        "product_id": product_id,
    }
    response = requests.post(url, json=json_req)
    st.write("success")

# Function to show more products
def show_more(product_name, query, category):
    url = "http://chat-be-service:8000/show-more/"
    json_req = {
        "query": query,
        "category": category
    }
    response = requests.post(url, json=json_req)
    for message in st.session_state.chat_history:
        if 'products' in  message and product_name in message['products']:
            message['products'][product_name].extend(response.json()['response']['products'])
# Main chat function
def chat():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'last_products' not in st.session_state:
        st.session_state.last_products = {}

    st.title("Chatbot Interface")

    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    col2, col3 = st.columns([7, 1])

    with col2:
        user_input = st.text_input("Type a message...", "")
    with col3:
        st.write(" ")
        st.write(" ")
        send = st.button("Send")

    if send:
        if user_input.strip() == "":
            st.warning("Please enter a message.")
        else:
            try:
                bot_response = send_message(prepare_messages(user_input), st.session_state.last_products, uploaded_file)
            except Exception as e:
                st.write(str(e))
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "bot", "content": bot_response["bot"], "products": bot_response["products"], "queries": bot_response["queries"]})
            user_input = ''

    # Display chat history with product card layout
    for entry in st.session_state.chat_history[::-1]:
        if entry["role"] == "user":
            st.markdown(
                f"<div style='display: flex; justify-content: flex-end; align-items: center; padding: 10px; border-radius: 10px; margin: 10px 0; background-color: #cce5ff;'>"
                f"{entry['content']}"
                f"<img src='https://api.dicebear.com/8.x/personas/svg?seed=Molly' style='width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;' />"  # User avatar
                f"</div>",
                unsafe_allow_html=True
            )
        elif entry["role"] == "bot":
            st.markdown(
                f"<div style='display: flex; justify-content: flex-start; align-items: center; padding: 10px; border-radius: 10px; margin: 10px 0; background-color: #f8d7da;'>"
                f"<img src='https://api.dicebear.com/8.x/bottts/svg?seed=Lucky' style='width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;' />"  # Bot avatar
                f"{entry['content']}"
                f"</div>",
                unsafe_allow_html=True
            )
            if entry["products"]:
                for product_name in entry["products"]:
                    st.markdown(f"<h2>{product_name}</h2>", unsafe_allow_html=True)

                    # Display products as cards with consistent image size
                    for product in entry["products"][product_name]:
                        image_html = image_interface(product['imageURLHighRes'])
                        card_content = (
                            f"<div class='product-card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 15px 0; background-color: #f9f9f9;'>"
                            f"  <div style='text-align: center;'>"
                            f"    {image_html}"  # Embed consistent-sized images within card
                            f"  </div>"
                            f"  <div style='margin-top: 10px;'>"
                            f"    <h3 style='color: #333; font-weight: bold;'>{product['title']}</h3>"
                            f"    <p style='color: #555; font-size: 14px; line-height: 1.5;'>{product['summary']}</p>"
                            f"    <p style='color: #888; font-size: 12px; font-style: italic;'>ASIN: {product['asin']}</p>"
                            f"  </div>"
                        )
                        st.markdown(card_content, unsafe_allow_html=True)

                        # Wishlist button
                        button_key = f"wishlist_{product['asin']}_{uuid4()}"
                        sound_file = BytesIO()
                        tts = gTTS(product['summary'], lang=    'en')
                        tts.write_to_fp(sound_file)
                        st.audio(sound_file)
                        st.button("❤️ Wishlist", key=button_key, on_click=lambda x: add_wishlist(x), args=[product['asin']])

                    # Show More button
                    if product_name in entry["queries"]:
                        product_cat = entry["products"][product_name][0].get("category", None)
                        show_more_button = f"show_more_{uuid4()}"
                        st.button(
                            "Show More",
                            key=show_more_button,
                            on_click=lambda pn, q, c: show_more(pn, q, c),
                            args=[product_name, entry["queries"][product_name], product_cat],
                            use_container_width=True,
                        )
        
        st.markdown("---")

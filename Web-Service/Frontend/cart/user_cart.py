import requests
import streamlit as st
from chat.message.images import image_interface
def prepare_messages(new_message):
    messages=[]
    if st.session_state.cart_chat_history:
        # st.write(st.session_state.chat_history)
        messages = st.session_state.cart_chat_history[-4:]
    messages.append({"role":"user","content": new_message})
    return messages
def send_message(messages, products):
    url = "http://chat-be-service:8000/cart-message/"
    # st.write(messages)    
    json_req = {
        "messages": messages,
        "products": products,
      }
    response = requests.post(url, json=json_req)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        st.error(f"Request failed with status code: {response}")

def get_wishlist():
    url = "http://chat-be-service:8000/get-cart/"
    json_req = {
        "userid": st.session_state.get('user_id', 1),
      }
    response = requests.get(url, params=json_req)
    return response.json()["response"]
def delete_wishlist(product_id):
    url = "http://chat-be-service:8000/delete-cart/"
    json_req = {
        "userid": st.session_state.get('user_id', 1),
        "product_id": product_id,
    }
    response = requests.post(url, json=json_req)
    st.write("success")

def wishlist_products():
    col0, col1 = st.columns(2)
    with col0:
        st.markdown("<h2 style='color: #333;'>Your Wishlisted Products ❤️ </h2>", unsafe_allow_html=True)
        products = get_wishlist()

        # Loop through each product and create a unique key for the remove button
        for index, product in enumerate(products):
            image_html = image_interface(product['imageURLHighRes'])

            # Product card
            st.markdown(
                f"<div class='product-card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 15px 0; background-color: #f9f9f9;'>"
                f"  <div style='text-align: center;'>"
                f"    {image_html}"
                f"  </div>"
                f"  <div style='margin-top: 10px;'>"
                f"    <h3 style='color: #333; font-weight: bold;'>{product['title']}</h3>"
                f"    <p style='color: #555; font-size: 14px; line-height: 1.5;'>{product['summary']}</p>"
                f"    <p style='color: #888; font-size: 12px; font-style: italic;'>ASIN: {product['asin']}</p>"
                f"  </div>"
                f"</div>",
                unsafe_allow_html=True
            )

            # Adding a unique key for each remove button
            st.button(
                "❌ Remove",
                key=f"remove-{index}-{product['asin']}",
                on_click=delete_wishlist,
                args=(product['asin'],),
            )
    st.write("---")
    with col1:
        st.markdown("<h3 style='color: #333;'>Ask me how to match your wishlisted products with other products !!!</h3>", unsafe_allow_html=True)
        col2, col3 = st.columns([5, 3])
        
        st.session_state.cart_chat_history = []
        with col2:
            user_input = st.text_input("Type a message...", "")
        with col3:
            st.write("")
            st.write("")
            send = st.button("Send")
        if send:
            if user_input.strip() == "":
                st.warning("Please enter a message.")
            else:
                    # st.text("senidng")
                try:
                    bot_response = send_message(prepare_messages(user_input),products )
                except Exception as e:
                    st.write(str(e))
                st.session_state.cart_chat_history.append({"role":"user", "content":user_input})  # Update chat history
                st.session_state.cart_chat_history.append({"role":"bot","content" : bot_response['bot'], "products":  bot_response['products']})    
                user_input = ''
            for idx, entry in enumerate(st.session_state.cart_chat_history[::-1]):
                    if entry["role"] == "user":
                        st.markdown(
                            f"<div style='display: flex; justify-content: flex-end; align-items: center; padding: 10px; border-radius: 10px; margin: 10px 0; background-color: #cce5ff;'>"
                            f"{entry['content']}"
                            f"<img src='https://api.dicebear.com/8.x/personas/svg?seed=Molly' style='width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;' />"  # User avatar
                            f"</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<div style='display: flex; justify-content: flex-start; align-items: center; padding: 10px; border-radius: 10px; margin: 10px 0; background-color: #f8d7da;'>"
                            f"<img src='https://api.dicebear.com/8.x/bottts/svg?seed=Lucky' style='width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;' />"  # Bot avatar
                            f"{entry['content']}"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                
                        # Display products given by bot in card format
                        for product in entry.get("products", []):
                            image_html = image_interface(product['imageURLHighRes'])
                            card_content = (
                                f"<div class='product-card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 15px 0; background-color: #f9f9f9;'>"
                                f"  <div style='text-align: center;'>"
                                f"    {image_html}"  # Embed consistent-sized images within card
                                f"  </div>"
                                f"  <div style='margin-top: 10px;'>"
                                f"    <h3 style='color: #333; font-weight: bold;'>{product['title']}</h3>"  # Product title with bold font
                                f"    <p style='color: #555; font-size: 14px; line-height: 1.5;'>{product['summary']}</p>"  # Product summary
                                f"    <p style='color: #888; font-size: 12px; font-style: italic;'>ASIN: {product['asin']}</p>"  # Product ASIN
                                f"  </div>"
                                f"</div>"
                            )
                            st.markdown(card_content, unsafe_allow_html=True)
                                
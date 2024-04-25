import streamlit as st
import requests
import os
import ast
# Importing original functionalities
from chat.chat_main import chat
from cart.user_cart import wishlist_products
from personalisation.user_suggestions import suggested_products
from image_search.image_search import search_image


# Load environment variables for FastAPI endpoint
FASTAPI_ENDPOINT = "http://chat-be-service:8000"

# Define activity options globally
activity_options = [
    "Reading", "Exercising", "Crafting", "Cooking and Baking", "Gardening",
    "Watching Movies/TV Shows", "Playing Video Games", "Listening to Music/Podcasts",
    "Social Media Browsing", "Traveling", "Photography", "Painting and Drawing",
    "Volunteering", "Attending Cultural Events", "Meditating", "Playing Sports",
    "Learning a New Skill", "Building Models/Puzzles", "Hiking and Nature Walks",
    "Writing and Journaling", "Others"
]

# Title with emojis
st.title("Market Mind: The Smart Way to Discover Products You'll Love 🛍️✨")

# Sidebar with navigation and image
def sidebar():
    st.sidebar.image("images/plogo.png", use_column_width=True)

    # Check if the user is logged in
    if "token" in st.session_state:
        st.sidebar.write(f"Welcome, {st.session_state.get('username', 'User')}!")
        # Navigation after login
        selection = st.sidebar.radio("Navigation", ["Chat", "Wishlist", "Suggested Products", "Search by Image"])

        # Logout button
        if st.sidebar.button("Logout"):
            del st.session_state["token"]
            del st.session_state["username"]
            st.success("Logged out successfully.")
            st.experimental_rerun()  # Refresh to clear session

        # Display selected page/component
        pages = {
            "Chat": chat,
            "Wishlist": wishlist_products,
            "Suggested Products": suggested_products,
            "Search by Image": search_image,
        }
        pages[selection]()

    else:
        # If not logged in, show login/signup options
        st.sidebar.write("Please login or signup.")

        tab1, tab2, tab3 = st.tabs(["About", "Login", "Signup"])

        with tab1:
            st.header("About This App")
            st.write("🎉 Welcome to Market Mind! 🛍️✨" )
            st.write("Step into the future of e-commerce with Market Mind, where cutting-edge analytics meet personalized shopping experiences. Our platform is more than just a tool—it's a game-changer in how businesses understand and respond to consumer needs and market trends.")
            st.write("Imagine having your own personal shopping assistant, available 24/7 to provide tailored product suggestions based on your preferences and past interactions. That's Market Mind for you! Our conversational interface makes it easy to input queries and receive highly relevant recommendations in real-time.")
            st.write("But Market Mind doesn't stop there. We go beyond simple suggestions by diving deep into personalised image search, recommendations from user activities to offer businesses invaluable insights into product performance and customer satisfaction.")
            st.write("What sets Market Mind apart is its accessibility. We've designed our platform with a user-friendly interface that simplifies complex data analysis, making big data insights accessible to businesses of all sizes.")
            st.write("Powered by robust cloud-based technologies, Market Mind ensures scalability and reliability, so you can trust that your data operations are in good hands.")
            st.write("Join us on this journey to revolutionize the e-commerce landscape. Welcome to Market Mind — where insights meet innovation, and every shopping experience is personalized just for you. 🚀")

        with tab2:
            st.header("Login Page")
            with st.form("login_form"):
                login_username = st.text_input("Username", key="login_username_1")
                login_password = st.text_input("Password", type="password", key="login_password_1")

                if st.form_submit_button("Login"):
                    login_data = {
                        "username": login_username,
                        "password": login_password,
                    }
                    response = requests.post(f"{FASTAPI_ENDPOINT}/login", json=login_data)
                    if response.status_code == 200:
                        st.success("Login successful!")
                        st.session_state["token"] = response.json().get("access_token")
                        st.session_state["username"] = login_username
                        st.session_state["user_id"] = response.json().get("user_id")
                        st.experimental_rerun()  # Refresh to show logged-in view
                    else:
                        st.error("Login failed! Please try again.")

        with tab3:
            st.header("Signup Page")
            with st.form("signup_form"):
                signup_username = st.text_input("Username", key="signup_username_1")
                signup_password = st.text_input("Password", type="password", key="signup_password_1")
                signup_gender = st.selectbox("Gender", ["Men", "Women"], key="signup_gender_1")
                signup_activities = st.multiselect("Select your activities", activity_options, key="signup_activities_1")

                if st.form_submit_button("Signup"):
                    signup_data = {
                        "username": signup_username,
                        "password": signup_password,
                        "gender": signup_gender,
                        "activities": signup_activities,
                    }
                    response = requests.post(f"{FASTAPI_ENDPOINT}/signup", json=signup_data)
                    if response.status_code == 200:
                        st.success("Signup successful!")
                    else:
                        st.error("Signup failed! Please try again.")

# Run the main Streamlit application
def main():
    sidebar()  # Display sidebar content

    # # Show default content if not logged in
    # if "token" not in st.session_state:
    #     st.header("Welcome to Market Mind")
    #     st.write("Please use the sidebar to login or signup.")

# Run the main function
if __name__ == "__main__":
    main()

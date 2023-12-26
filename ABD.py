import streamlit as st
import google.generativeai as palm
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

API_KEY = os.environ.get("PALM_API_KEY")
palm.configure(api_key=API_KEY)

def is_user_logged_in():
    return st.session_state.get("logged_in", False)

def perform_login(username, password):
    return username == "user" and password == "123"

def initiate(user_input):
    prompt = """
    I will give you the symptoms of the disease
    explain what diseases I might suffer from and how to deal with them
    act like a health assistant
    don't answer if the question is not about health or diseases
    """ + "i have ", user_input

    response = palm.chat(messages=user_input)
    return response

def reply(prev_msg, user_input):
    return prev_msg.reply(user_input)

def display_response(response):
    for message in response.messages:
        author_name = "Human" if message['author'] == '0' else "Health Assistant"
        st.markdown(f"**{author_name}:** {message['content']}", unsafe_allow_html=True)

def main():
    
    if not is_user_logged_in():
        st.image("mh.png", use_column_width=True, width=300, output_format="auto")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Log in"):
            if perform_login(username, password):
                st.session_state.logged_in = True
            else:
                st.error("Invalid login credentials. Please try again.")
    else:
        
        st.sidebar.header("Menu")
        
        # Tampilkan menu pilihan setelah login
        menu_choice = st.sidebar.selectbox("Choose an option", ["Chatbot","Pharmacy", "Reminder", "Doctor Appointment"])
        
        if menu_choice == "Chatbot":
            st.image("hc.png", use_column_width=True, width=300, output_format="auto")
            st.write("")
            st.header("Chat with Your Health Assistant")
            st.write("")

            prompt = st.text_input("Describe your medical symptoms:", placeholder="Enter your symptoms here...", label_visibility="visible")

            if st.button("SEND", use_container_width=True):
                if "prev_msg" not in st.session_state:
                    response = initiate(prompt)
                else:
                    response = reply(st.session_state.prev_msg, prompt)

                st.session_state.prev_msg = response

                st.write("")
                st.header(":blue[Response]")
                st.write("")

                display_response(response)

        elif menu_choice == "Pharmacy":
            st.image("phr.png", use_column_width=True, width=300, output_format="auto")

            st.image("prctm.png", use_column_width=True, width=50, output_format="auto")
            st.write("Paracetamol")
            st.write("Price: Rp. 10.000")

            if st.button("Add To Cart"):
                st.success("Successfully Added to Cart")
        
        elif menu_choice == "Reminder":
            st.image("hr.png", use_column_width=True, width=300, output_format="auto")
            st.header("Set a Reminder")
            # Tambahkan logika untuk setting reminder di sini
            
            reminder_text = st.text_input("Enter reminder text:")
            reminder_date = st.date_input("Select reminder date", min_value=datetime.date.today())
            reminder_time = st.time_input("Select reminder time")

            if st.button("Set Reminder"):
                # Tambahkan logika untuk menetapkan pengingat di sini
                st.success("Reminder set successfully!")

        elif menu_choice == "Doctor Appointment":
            st.image("da.png", use_column_width=True, width=300, output_format="auto")
            st.header("Sorry! This Page Is Under Construction")

if __name__ == "__main__":
    main()

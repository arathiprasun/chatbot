import streamlit as st
import random
import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize Google Sheets credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(".streamlit/secrets.json", scope)
client = gspread.authorize(creds)
chat_history_sheet = client.open("ChatHistory").sheet1
user_responses_sheet = client.open("UserResponses").sheet1

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Store user and assistant messages in Google Sheets
    user_message = prompt
    assistant_message = full_response
    chat_history_sheet.append_row([user_message, assistant_message])

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Store user response in Google Sheet for user responses
    user_responses_sheet.append_row([user_message])

# Update chat history and user responses
st.session_state.messages.append({"role": "user", "content": user_message})

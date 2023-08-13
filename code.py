import streamlit as st
import random
import time
from google.cloud import storage
import json
from datetime import datetime

st.title("Simple chat")

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'your-bucket-name'
object_prefix = 'chat-messages/'

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

        # Upload assistant response to Google Cloud Storage
        user_id = 'assistant'
        upload_message(user_id, full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Upload a new chat message
def upload_message(user_id, message):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    object_name = f'{object_prefix}{user_id}_{timestamp}.json'

    message_data = {
        'user_id': user_id,
        'message': message,
        'timestamp': timestamp
    }

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(json.dumps(message_data))

# Example usage
user_id = '123'
message = 'Hello, how are you?'
upload_message(user_id, message)

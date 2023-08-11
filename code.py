
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
recognizer = sr.Recognizer()
microphone = sr.Microphone()
def main():
    st.title("Voice Bot")

    # Add a button to start voice input
    if st.button("Start Recording"):
        with microphone as source:
            st.write("Listening...")
            audio = recognizer.listen(source)
            st.write("Processing...")

            try:
                # Recognize the audio
                user_input = recognizer.recognize_google(audio)
                st.write(f"You said: {user_input}")

                # Process user input and generate a response
                response = process_user_input(user_input)

                # Generate an audio response using gTTS
                tts_response = gTTS(response)
                st.audio(tts_response)

            except sr.UnknownValueError:
                st.write("Sorry, I couldn't understand you.")
            except sr.RequestError as e:
                st.error(f"Could not request results: {e}")

if __name__ == "__main__":
    main()

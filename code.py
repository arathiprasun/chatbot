import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech

# Initialize Google Cloud clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Create Streamlit UI
st.title("Voicebot")

# Define voice command input
user_input = st.text_input("Speak a voice command", "")

# Process user input and provide response
if st.button("Process"):
    # Convert user input to speech recognition audio
    recognition_audio = speech.RecognitionAudio(content=user_input.encode())

    # Configure speech recognition request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Request speech-to-text transcription
    response = speech_client.recognize(config=config, audio=recognition_audio)

    # Extract transcript from the response
    transcript = response.results[0].alternatives[0].transcript

    # Use the transcript to generate a response
    if "hello" in transcript:
        response_text = "Hello there!"
    else:
        response_text = "Sorry, I didn't understand that."

    # Convert response text to speech
    tts_input = texttospeech.SynthesisInput(text=response_text)
    tts_voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    tts_audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    tts_response = tts_client.synthesize_speech(
        input=tts_input, voice=tts_voice, audio_config=tts_audio_config
    )

    # Display response text and play the synthesized speech
    st.text_area("Response", value=response_text)
    st.audio(tts_response.audio_content, format="audio/wav")

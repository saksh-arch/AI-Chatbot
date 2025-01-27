import pyttsx3
import speech_recognition as sr
from langchain import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import streamlit as st
import threading
import hashlib
from textblob import TextBlob


load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
langsmith_api = os.getenv('LANGCHAIN_API_KEY')


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)


prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "You are a helpful assistant that gives only the required answer in one or two short sentences.\n\n"
        "Avoid unnecessary details.\n\n"
        "Conversation History:\n{history}\n\n"
        "User's Question:\n{input}\n\n"
        "Answer:"
    ),
)

memory = ConversationBufferMemory()
conversation = ConversationChain(prompt=prompt, llm=llm, memory=memory)


tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[1].id)


def speak(text):
    """Convert text to speech in a separate thread."""
    def run_tts():
        tts_engine = pyttsx3.init()
        voices = tts_engine.getProperty('voices')
        tts_engine.setProperty('voice', voices[1].id)  # Adjust voice if needed
        tts_engine.say(text)
        tts_engine.runAndWait()
    
    tts_thread = threading.Thread(target=run_tts)
    tts_thread.start()


def analyze_sentiment(text):
    """Analyze the sentiment of the text using TextBlob."""
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 to 1 range, -1 is negative, 1 is positive
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"


def listen():
    """Listen to the user's voice input and analyze sentiment."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            sentiment = analyze_sentiment(user_input)
            st.write(f"Sentiment: {sentiment.capitalize()}")
            return user_input, sentiment
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Could you please repeat?", "neutral"
        except sr.RequestError:
            return "Sorry, there seems to be an issue with the speech recognition service.", "neutral"




if "users" not in st.session_state:
    st.session_state["users"] = {}
if "conversation_topics" not in st.session_state:
    st.session_state["conversation_topics"] = {}
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "current_topic" not in st.session_state:
    st.session_state["current_topic"] = "General"

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function to validate login credentials
def validate_login(username, password):
    hashed_password = hash_password(password)
    return st.session_state["users"].get(username) == hashed_password


# Function to handle signup
def signup_user(username, password):
    if username in st.session_state["users"]:
        return False     # Username already exists
    st.session_state["users"][username] = hash_password(password)
    st.session_state["conversation_topics"][username] = {}  # Initialize topic storage for the user
    return True


# Function to switch pages
def switch_page(page_name):
    st.session_state["current_page"] = page_name


# Main Function for Login Page
def login_page():
    st.title("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_login(username, password):
            st.success(f"Welcome back, {username}!")
            st.session_state["authenticated"] = True
            st.session_state["current_user"] = username
            switch_page("Chatbot")
        else:
            st.error("Invalid username or password. Please try again.")
    st.button("New User? Signup Here", on_click=lambda: switch_page("Signup"))


# Main Function for Signup Page
def signup_page():
    st.title("🔒 Signup")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Signup"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif signup_user(new_username, new_password):
            st.success("Account created successfully! Please log in.")
            switch_page("Login")
        else:
            st.error("Username already exists. Please choose a different one.")
    st.button("Already have an account? Login Here", on_click=lambda: switch_page("Login"))


# Main Function for Chatbot Page
def chatbot_page():
    st.title("🤖 AI Chatbot Assistant")
    st.markdown("<h3 style='color:#FF6347;'>Chat with your AI assistant</h3>", unsafe_allow_html=True)
    st.markdown("---")

    username = st.session_state["current_user"]

    # Dark Mode Toggle
    dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
    if dark_mode:
        st.markdown(
            """
            <style>
            body { background-color: #121212; color: #ffffff; }
            .stTextInput input { background-color: #333; color: #fff; }
            .stButton>button { background-color: #444; color: #fff; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Topic selection
    user_topics = st.session_state["conversation_topics"].get(username, {})
    topic_list = list(user_topics.keys())
    st.session_state["current_topic"] = st.selectbox("Select or Create a Topic", topic_list + ["New Topic"], index=0)
    
    if st.session_state["current_topic"] == "New Topic":
        new_topic = st.text_input("Enter New Topic Name:")
        if st.button("Create Topic") and new_topic:
            st.session_state["conversation_topics"][username][new_topic] = []
            st.session_state["current_topic"] = new_topic

    # Get current topic history
    current_topic = st.session_state["current_topic"]
    if current_topic not in user_topics:
        st.session_state["conversation_topics"][username][current_topic] = []

    # Input method
    input_method = st.sidebar.radio("Select Input Method:", ("Text", "Voice"))

    # Text input section
    if input_method == "Text":
        user_input = st.text_input("Type your message:", key="user_input")
    else:
        user_input, sentiment = listen()

    if user_input:
        # Process user input
        response = conversation.invoke(input=user_input)
        response_text = response["response"]

        # Save conversation to topic
        st.session_state["conversation_topics"][username][current_topic].append((user_input, response_text))

        # Display the conversation
        st.markdown("### Conversation History")
        for user_msg, bot_msg in st.session_state["conversation_topics"][username][current_topic]:
            st.write(f"**You:** {user_msg}")
            st.write(f"**Chatbot:** {bot_msg}")

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        switch_page("Login")




if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Login"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["current_page"] == "Login":
    login_page()
elif st.session_state["current_page"] == "Signup":
    signup_page()
elif st.session_state["current_page"] == "Chatbot" and st.session_state["authenticated"]:
    chatbot_page()
else:
    st.session_state["current_page"] = "Login"
    login_page()

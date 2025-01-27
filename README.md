# AI Chatbot 

This project is an AI-powered chatbot that uses natural language processing to facilitate user interaction. The chatbot supports both
text and voice inputs, provides sentiment analysis,and includes user authentication features.

---

## Features

- **Voice and Text Input:** Users can interact with the chatbot using either text or voice.
- **Sentiment Analysis:** Analyzes user input sentiment (positive, negative, or neutral) using TextBlob.
- **User Authentication:** Includes a secure login and signup system with hashed passwords.
- **Conversation Topics:** Organize conversations by topics for better context management.
- **Dark Mode:** User-friendly dark mode toggle for improved accessibility.
- **Streamlit-Based UI:** Interactive and responsive interface built with Streamlit.
- **Text-to-Speech:** Converts chatbot responses to speech using `pyttsx3`.

---

## Technologies Used

- **Streamlit:** Frontend interface for the chatbot.
- **LangChain Framework:** Handles conversation flow and AI response generation.
- **Google Generative AI (Gemini):** Provides AI responses via the `langchain_google_genai` module.
- **TextBlob:** Performs sentiment analysis.
- **SpeechRecognition:** Enables voice input from users.
- **pyttsx3:** Implements text-to-speech functionality.
- **dotenv:** Manages API keys and environment variables securely.
- **Hashlib:** Hashes user passwords for secure authentication.

---

## Prerequisites

1. **Python 3.8+** installed on your system.
2. Install dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file to store your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/saksh-arch/AI-Chatbot.git
   ```
2. Navigate to the project directory:
   ```bash
   cd AI-Chatbot
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

---

## Project Structure

```
AI-Chatbot/
├── app.py              # Main application file
├── .env                # Environment variables (not included in the repository)
├── LICENSE             # MIT License
├── README.md           # Project documentation
├── .gitignore          # Files to ignore in Git
└── requirements.txt    # Python dependencies
```

---

## Features Overview

### Authentication
- Users can sign up and log in securely with hashed passwords.

### Conversation Topics
- Organize chats by topics to keep conversations contextually relevant.

### Input Options
- Choose between typing or speaking your message.

### Sentiment Analysis
- Analyzes the sentiment of user messages in real-time.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- 

Thank you !


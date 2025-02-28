import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import os
from pathlib import Path

# Ensure NLTK data is available
nltk_data_dir = os.path.join(Path.home(), "nltk_data")
if not os.path.exists(nltk_data_dir):
    nltk.download("punkt", download_dir=nltk_data_dir)
    nltk.download("stopwords", download_dir=nltk_data_dir)
    nltk.download("wordnet", download_dir=nltk_data_dir)
nltk.data.path.append(nltk_data_dir)


class ChatBot:
    def __init__(self, name="Chatbot"):
        self.name = name
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        self.memory = {"last_input": "", "last_tokens": [], "context": []}
        self.greetings = ["Hello!", "Hi there!", "Hey!", "Greetings!"]
        self.farewells = ["Goodbye!", "See you later!", "Bye!", "Take care!"]

        self.responses = {
            "what is your name?": "I am a simple chatbot.",
            "what is the capital of france?": "The capital of France is Paris.",
            "how many days are in a year?": "There are 365 days in a regular year and 366 in a leap year.",
            "what is the largest planet in our solar system?": "Jupiter is the largest planet.",
            "what is the square root of 144?": "The square root of 144 is 12.",
            "what is the meaning of life?": "That's a philosophical question! There's no single answer.",
            "what is the weather like today?": "I don't have access to real-time information, including weather.",
            "what is the speed of light?": "The speed of light is approximately 299,792,458 meters per second.",
            "who painted the mona lisa?": "Leonardo da Vinci painted the Mona Lisa.",
            "what is the chemical symbol for water?": "The chemical symbol for water is H2O.",
            "what is the chemical symbol for gold?": "The chemical symbol for gold is Au.",
            "what is the largest ocean?": "The Pacific Ocean is the largest.",
            "what is the currency of japan?": "The currency of Japan is the Yen.",
            "what is the population of india?": "I do not have access to real time data, population numbers change frequently.",
            "what is a prime number?": "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.",
            "what is the distance to the moon?": "The average distance to the moon is about 384,400 kilometers.",
            "what are the primary colors?": "The primary colors are red, blue, and yellow.",
            "what is the boiling point of water?": "The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit).",
            "what is the largest mammal?": "The blue whale is the largest mammal.",
            "what is the hardest natural substance?": "Diamond is the hardest natural substance.",
            "what is the formula for the area of a circle?": "The formula for the area of a circle is πr².",
        }

    def process_input(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and token.isalnum()
        ]
        return tokens, text.lower()

    def get_response(self, user_input):
        tokens, raw_input = self.process_input(user_input)
        self.memory["last_input"] = user_input
        self.memory["last_tokens"] = tokens
        self.memory["context"].append(tokens)
        if len(self.memory["context"]) > 3:
            self.memory["context"].pop(0)

        if raw_input in ["bye", "exit", "quit"]:
            return random.choice(self.farewells)

        matches = []
        for question, response in self.responses.items():
            question_tokens = set(word_tokenize(question.lower()))
            input_tokens = set(tokens)
            match_count = len(question_tokens & input_tokens)
            if match_count > 0:
                context_bonus = sum(
                    1
                    for past_tokens in self.memory["context"][:-1]
                    if any(t in question_tokens for t in past_tokens)
                )
                matches.append((match_count + context_bonus * 0.5, response))

        if matches:
            matches.sort(reverse=True)
            return matches[0][1]

        return random.choice(
            [
                "Interesting! Tell me more.",
                "I don’t have an answer for that yet. Try something else!",
            ]
        )


# Streamlit app
st.title("Chatbot")
st.write("Built by Chandana - Ask me anything!")

# Initialize chatbot and chat history
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot()
    st.session_state.chat_history = [
        (None, random.choice(st.session_state.chatbot.greetings))
    ]
if "input_text" not in st.session_state:
    st.session_state.input_text = ""  # Store input text

# Display chat history
for user_msg, bot_msg in st.session_state.chat_history:
    if user_msg:
        st.write(f"**You**: {user_msg}")
    st.write(f"**{st.session_state.chatbot.name}**: {bot_msg}")

# Form for Enter key submission
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your message:", value=st.session_state.input_text, key="user_input"
    )
    submit_button = st.form_submit_button(label="Send")

# Handle submission (Enter key or button)
if submit_button and user_input:
    response = st.session_state.chatbot.get_response(user_input)
    st.session_state.chat_history.append((user_input, response))
    st.session_state.input_text = ""  # Clear input
    st.rerun()  # Refresh to update chat

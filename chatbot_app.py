import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import os

# Use bundled NLTK data
nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_dir)

class ChatBot:
    def __init__(self, name="Chatbot"):
        self.name = name
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.memory = {'last_input': '', 'last_tokens': [], 'context': []}
        self.greetings = ["Hello!", "Hi there!", "Hey!", "Greetings!"]
        self.farewells = ["Goodbye!", "See you later!", "Bye!", "Take care!"]
        
        self.responses = {
            "what is your name": "I am a simple chatbot.",
            "what is the chemical symbol for water": "The chemical symbol for water is H2O.",
            "what is the chemical symbol for gold": "The chemical symbol for gold is Au.",
            "what is the largest mammal": "The blue whale is the largest mammal."
        }

    def process_input(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and token.isalnum()]
        return tokens, text.lower()

    def get_response(self, user_input):
        tokens, raw_input = self.process_input(user_input)
        self.memory['last_input'] = user_input
        self.memory['last_tokens'] = tokens
        self.memory['context'].append(tokens)
        if len(self.memory['context']) > 3:
            self.memory['context'].pop(0)
        
        if raw_input in ['bye', 'exit', 'quit']:
            return random.choice(self.farewells)

        matches = []
        for question, response in self.responses.items():
            question_tokens = set(word_tokenize(question.lower()))
            input_tokens = set(tokens)
            match_count = len(question_tokens & input_tokens)
            if match_count > 0:
                context_bonus = sum(1 for past_tokens in self.memory['context'][:-1] 
                                  if any(t in question_tokens for t in past_tokens))
                matches.append((match_count + context_bonus * 0.5, response))
        
        if matches:
            matches.sort(reverse=True)
            return matches[0][1]
        
        return random.choice([
            "Interesting! Tell me more.",
            "I don’t have an answer for that yet. Try something else!"
        ])

st.title("Chatbot Web App")
st.write("Built by [Your Institute Name] - Ask me anything!")

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot()
    st.session_state.chat_history = [(None, random.choice(st.session_state.chatbot.greetings))]
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

for user_msg, bot_msg in st.session_state.chat_history:
    if user_msg:
        st.write(f"**You**: {user_msg}")
    st.write(f"**{st.session_state.chatbot.name}**: {bot_msg}")

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message:", value=st.session_state.input_text, key="user_input")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    response = st.session_state.chatbot.get_response(user_input)
    st.session_state.chat_history.append((user_input, response))
    st.session_state.input_text = ""
    st.rerun()
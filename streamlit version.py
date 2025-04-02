import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the client with your API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Custom CSS for Arabic chat interface
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #6a38a0, #1c1e21);
        color: white;
        text-align: center;
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    .user-message {
        background: #7a3636;
        color: white;
        border-radius: 15px 15px 0 15px;
        padding: 10px;
        margin: 5px;
        max-width: 75%;
        float: right;
        clear: both;
    }
    .bot-message {
        background: #2c3e50;
        color: white;
        border-radius: 15px 15px 15px 0;
        padding: 10px;
        margin: 5px;
        max-width: 75%;
        float: left;
        clear: both;
    }
    .stTextInput>div>div>input {
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🤖 شات بوت")

# Display chat messages
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f'<div class="{message["role"]}-message">{message["content"]}</div>', 
                       unsafe_allow_html=True)

# User input
if prompt := st.chat_input("💬 اكتب رسالتك هنا..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">🧑‍💻 : {prompt}</div>', unsafe_allow_html=True)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown('<div class="bot-message">🤖 البوت يكتب... ⏳</div>', 
                                   unsafe_allow_html=True)
        
        try:
            # Call the API
            response = client.chat.completions.create(
                model="meta-llama/llama-3.2-1b-instruct:free",
                messages=[{"role": m["role"], "content": m["content"]} 
                         for m in st.session_state.messages]
            )
            
            full_response = response.choices[0].message.content
            # Clean up the response
            full_response = full_response.replace(/[{}]/g, "").replace(/\\boxed\s*/g, "").trim()
            
            # Update the placeholder with the actual response
            message_placeholder.markdown(
                f'<div class="bot-message">🤖 : {full_response}</div>', 
                unsafe_allow_html=True
            )
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            message_placeholder.markdown(
                '<div class="bot-message">⚠️ خطأ: لا يمكن الاتصال بالخادم.</div>', 
                unsafe_allow_html=True
            )
            st.error(f"Error: {str(e)}")

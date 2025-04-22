import streamlit as st
from streamlit_chat import message
import requests
import re  # Added for regex handling
import time

st.set_page_config(
    page_title="شات بوت بالعربية",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #6a38a0, #1c1e21);
        color: white;
    }
    .stTextInput>div>div>input {
        color: white;
        background-color: rgba(255, 255, 255, 0.2);
    }
    .stButton>button {
        background-color: #ff9800;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e68900;
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state.generated = []
if 'past' not in st.session_state:
    st.session_state.past = []

st.title("🤖 شات بوت")

def get_bot_response(user_input):
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-website.com",  # Update with your URL
        "X-Title": "Arabic Chatbot"  # Update with your app name
    }
    payload = {
        "model": "meta-llama/llama-3-70b-instruct",  # Updated to current model name
        "messages": [{"role": "user", "content": user_input}]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        bot_reply = data['choices'][0]['message']['content']
        # Fixed regex syntax for Python
        return re.sub(r'[{}]', '', re.sub(r'\\boxed\s*', '', bot_reply)).strip()
    except requests.exceptions.RequestException as e:
        return f"⚠️ خطأ في الاتصال: {str(e)}"
    except KeyError:
        return "⚠️ خطأ في معالجة الرد من الخادم"
    except Exception as e:
        return f"⚠️ خطأ غير متوقع: {str(e)}"

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)-1, -1, -1):
            message(st.session_state.generated[i], key=str(i), is_user=False)
            message(st.session_state.past[i], is_user=True, key=str(i) + '_user')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input form
with st.form(key='chat_form', clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("💬 اكتب رسالتك هنا...", key='input', value="")
    with col2:
        submit_button = st.form_submit_button(label='إرسال 🚀')
    
    if submit_button and user_input:
        st.session_state.past.append(user_input)
        
        with st.spinner("🤖 البوت يكتب... ⏳"):
            bot_response = get_bot_response(user_input)
            st.session_state.generated.append(bot_response)
        
        st.experimental_rerun()

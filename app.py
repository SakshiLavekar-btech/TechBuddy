# app.py
import streamlit as st
from ai import get_fast_study_buddy_stream
import gtts
import base64
from io import BytesIO

st.set_page_config(page_title="Tech Friend", page_icon="⚡")
st.title("⚡ Fast Tech Friend & Study Buddy")
st.write("Hey! I'm ready. Type anything and I will answer instantly! 🚀")

# Helper function to generate quick audio without slowing down the chat interface
def play_audio(text):
    try:
        tts = gtts.gTTS(text=text, lang='en', tld='co.in') # Friendly accent
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        # Injects an invisible audio player that plays immediately
        md = f'<audio src="data:audio/mp3;base64,{b64}" autoplay hidden></audio>'
        st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat elements
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input Box
if user_query := st.chat_input("Ask me anything..."):
    
    # 1. Print and save user input
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 2. Stream the AI response in real-time (Zero waiting time!)
    with st.chat_message("assistant"):
        # st.write_stream consumes the Python generator instantly
        full_response = st.write_stream(get_fast_study_buddy_stream(list(st.session_state.messages)))
            
    # 3. Save assistant message to memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # 4. Speak out the response seamlessly
    play_audio(full_response)

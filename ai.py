import streamlit as st
from freeGPT import AsyncClient
from asyncio import run
from PIL import Image
from io import BytesIO
import re  # Import the regular expression module

# Add custom CSS to fix the input bar at the bottom
st.markdown(
    """
    <style>
    .st-eb {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 999;
    }
    div.st-emotion-cache-zt5igj.e1nzilvr4{
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Exypni AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your message"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    async def chat_response(prompt):
     try:
        if prompt.lower().startswith("image of ") or prompt.lower().startswith("generate an image of ") or prompt.lower().startswith("create an image of "):
            resp = await AsyncClient.create_generation("prodia", prompt)
            image = Image.open(BytesIO(resp))
            st.image(image, caption="Generated Image", use_column_width=True)
            return "🤖: Image generated! And Will Disappear after Your next message"
        elif "your name" in prompt.lower():
            return " My name is GPTBuddy. An smart ai assistant which can do several tasks like generation, writing, coding, and much more."
        elif "who are you?" in prompt.lower():
            return " I am GPTBuddy. An smart ai assistant which can do several tasks like generation, writing, coding, and much more."
        else:
            resp = await AsyncClient.create_completion("gpt3", prompt)

            # Check if the generated response contains HTML tags
            if re.search(r'<.*?>', resp):
                # Execute the HTML code
                st.markdown(resp, unsafe_allow_html=True)
                return "🤖: HTML code executed!"
            else:
                return resp
     except Exception as e:
        return str(e)

    # Use Streamlit Async API to make the async function call
    with st.spinner("AI is processing your message..."):
        response = run(chat_response(prompt))

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add user and assistant responses to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

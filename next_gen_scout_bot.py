import os

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="")

ASSISTANT_ID = ""


def get_bot_response(user_input):
    """Get a response from the bot based on the user input using the Assistants API."""
    try:
        # thread = client.beta.threads.retrieve("thread_3dhXdai2l4vQQg3fCzC6YZXN")
        thread = client.beta.threads.create()

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        messages = client.beta.threads.messages.list(thread_id=thread.id)

        for message in reversed(messages.data):
            if message.role == "assistant":
                return message.content[0].text.value

        return "I couldn't generate a response. Please try again."

    except Exception as e:
        print(f"Error: {e}")
        return "I'm having trouble understanding that right now. Please try again later."


def run_app():
    """Run the Streamlit app."""
    st.title("NextGenScout Chatbot")
    st.markdown("Welcome to the NextGenScout Chatbot. Please type your message below to start the conversation!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form("user_input_form", clear_on_submit=True):
        user_input = st.text_area("Your Message:", height=150)
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        bot_response = get_bot_response(user_input)
        st.session_state.messages.append({"user": user_input, "bot": bot_response})

    for message in reversed(st.session_state.messages):
        user_message = f"""<div style="background-color: #f1f1f1; padding: 10px; border-radius: 5px; margin-bottom: 
        10px;"> <b>User:</b> <pre>{message['user']}</pre>
                           </div>"""
        bot_message = f"""<div style="background-color: #e8e8e8; padding: 10px; border-radius: 5px; margin-bottom: 
        10px;"> <b>Bot:</b> <pre>{message['bot']}</pre>
                          </div>"""

        st.write(user_message, unsafe_allow_html=True)
        st.write(bot_message, unsafe_allow_html=True)


if __name__ == "__main__":
    run_app()

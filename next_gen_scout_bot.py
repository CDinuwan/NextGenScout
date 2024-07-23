import streamlit as st
import openai
import json
import os

# Load your OpenAI API key from an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Function to load JSON data
def load_json_data(filepath):
    """Load JSON data from a file."""
    with open(filepath) as file:
        return json.load(file)


# Function to get bot response
def get_bot_response(user_input, json_data):
    """Get a response from the bot based on the user input and relevant JSON data."""
    try:
        relevant_data_str = json.dumps(json_data, indent=2)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"User input: {user_input}\nRelevant data: {relevant_data_str}"}
            ],
            max_tokens=150,
            temperature=0.7,
            api_key=OPENAI_API_KEY
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "I'm having trouble understanding that right now. Please try again later."


# Main function to run the Streamlit app
def run_app():
    """Run the Streamlit app."""
    st.title("NextGenScout Chatbot")
    st.markdown("Welcome to the NextGenScout Chatbot. Please type your message below to start the conversation!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    json_data = load_json_data("processed_data.json")

    with st.form("user_input_form", clear_on_submit=True):
        user_input = st.text_area("Your Message:", height=150)
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        bot_response = get_bot_response(user_input, json_data)
        st.session_state.messages.append({"user": user_input, "bot": bot_response})

    for message in st.session_state.messages:
        st.markdown(f'**User:**\n{message["user"]}')
        st.markdown(f'**Bot:**\n{message["bot"]}')


if __name__ == "__main__":
    run_app()

import streamlit as st
import time

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI Layout
st.set_page_config(page_title="ChatGPT Clone", layout="wide")

st.title("💬 ChatGPT Clone with Loader")
st.write("A fully functional Streamlit chat interface with a typing indicator.")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
if user_input := st.chat_input("Ask me anything..."):
    # Store user message in session
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display typing indicator (loader)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Create a placeholder
        message_placeholder.markdown("🤖 *Typing...*")  # Show loader text

        # Simulate a delay (Replace this with an actual AI API call)
        time.sleep(5)

        # Generate AI response (mock response, reversing text as a placeholder)
        ai_response = f"🤖 AI says: {user_input[::-1]}"

        # Update placeholder with AI response
        message_placeholder.markdown(ai_response)

    # Store AI response in session
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

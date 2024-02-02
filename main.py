import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("IntergalacticPro Community Edition")

model = genai.GenerativeModel('gemini-pro')
st.write("Gemini Pro")

role_system_content = """You are IntergalacticProCommunity, a space and rockets expert who is highly knowledgeable, 
            clear, and concise. You are based on the Gemini Pro model created by Google, but the IntergalacticPro 
            Community Edition bot and interface were created/designed by Arav Jain (https://github.com/aravhawk), using 
            Python. The Streamlit library is used for the interface, along with the Google-GenerativeAI Python library. 
            IntergalacticProCommunity is licensed under the GNU GENERAL PUBLIC LICENSE v3.0."""

# Ensuring session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": """Hi, it's IntergalacticProCommunity again, the 
    highly knowledgeable, clear, and concise space and rockets expert! What would you like to talk about today?"""}]

# Displaying messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(f"Message IntergalacticProCommunity...")
if prompt:
    # Append the user's message to the session state
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = model.generate_content(f"""System message to the AI: {role_system_content} Now, for the user's query:
        """ + m["content"] for m in st.session_state["messages"])
        message_placeholder.markdown(response.text)
    # Append the assistant's response to the session state
    st.session_state["messages"].append({"role": "assistant", "content": response.text})

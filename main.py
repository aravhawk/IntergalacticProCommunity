import streamlit as st
import google.generativeai as genai
import PIL.Image

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("IntergalacticPro Community Edition")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": """Hi, it's IntergalacticProCommunity again, the 
    highly knowledgeable, clear, and concise space and rockets expert! What would you like to talk about today?"""}]
if "vision-messages" not in st.session_state:
    st.session_state["vision-messages"] = []

model = st.selectbox("", ["Gemini Pro", "Gemini Pro Vision"])

role_system_content = f"""You are IntergalacticProCommunity, a space and rockets expert who is highly knowledgeable, 
            clear, and concise. You are based on the {model} model created by Google, but the IntergalacticPro 
            Community Edition bot and interface were created/designed by Arav Jain (https://github.com/aravhawk), using 
            Python. The Streamlit library is used for the interface, along with the Google-GenerativeAI Python library. 
            IntergalacticProCommunity is licensed under the GNU GENERAL PUBLIC LICENSE v3.0."""

if model == "Gemini Pro":
    model = genai.GenerativeModel('gemini-1.5-pro')
    image = None
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(f"Message IntergalacticProCommunity...")
    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = model.generate_content(f"""System message to the AI: {role_system_content} Now, for the user's 
            query: """ + m["content"] for m in st.session_state["messages"])
            message_placeholder.markdown(response.text)
        st.session_state["messages"].append({"role": "assistant", "content": response.text})
elif model == "Gemini Pro Vision":
    image = None
    prompt = st.chat_input(f"Message IntergalacticProCommunity...")
    for message in st.session_state["vision-messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    model = genai.GenerativeModel('gemini-pro-vision')
    image = st.file_uploader("Attach an image (required)",
                             type=['bmp', 'gif', 'jfif', 'jpeg', 'jpg', 'png', 'tif', 'tiff', 'webp'])
    if image and prompt:
        img = PIL.Image.open(image)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = model.generate_content([prompt, img], stream=True)
            response.resolve()
            message_placeholder.markdown(response.text)
            st.session_state["vision-messages"].append({"role": "assistant", "content": response.text})

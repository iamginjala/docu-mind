import streamlit as st
import requests

st.title("Docu-mind")

uploaded_files = st.file_uploader(
    "Upload pdf/text files", accept_multiple_files=True, type=["pdf","txt"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_files and not st.session_state.get("uploaded"):
    st.session_state.uploaded = True
    files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
    with st.spinner("Processing your documents..."):
        r = requests.post("http://backend:8000/upload", files=files)

        if r.status_code == 200:
            st.success("files processed sucessfully")
        
        else:
            st.error("error uploading files")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Reply...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    payload = {
        'ques':prompt,
        'chat_history': st.session_state.messages
    }
    response = requests.post("http://backend:8000/ask",json= payload)
    answer = response.json()["answer"]
    with st.chat_message("assistant"):
        st.write(answer)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": answer})
import streamlit as st

from langchain.memory import ConversationBufferMemory
from utils import qa_agent

st.title("AI PDF Reader")

with st.sidebar:
    openai_api_key = st.text_input("Enter OpenAI API password: ", type="password")
    st.markdown("[get OpenAI API password](https://openai.com/index/openai-api/)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True,
                                                          memory_key="chat_history",
                                                          output_key="answer"
                                                          )

if "clear_history_pressed" not in st.session_state:
    st.session_state["clear_history_pressed"] = False

uploaded_file = st.file_uploader("upload your file", type="pdf")
question = st.text_input("enter your question", disabled=not uploaded_file)

if uploaded_file and question and not openai_api_key:
    st.info("enter your openai api")
    st.stop()

if uploaded_file and not question and openai_api_key:
    st.info("enter your question")
    st.stop()

if uploaded_file and question and openai_api_key:
    with st.spinner("ai is thinking..."):
        response = qa_agent(openai_api_key, st.session_state["memory"], uploaded_file, question)

    st.write("### answer: ")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

if st.button("Clear History"):
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True,
                                                          memory_key="chat_history",
                                                          output_key="answer"
                                                          )
    st.session_state["chat_history"] = []
    st.session_state["clear_history_pressed"] = True
    st.stop()


if "chat_history" in st.session_state:
    with st.expander("Chat History"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i < (len(st.session_state["chat_history"]) - 2):
                st.divider()

# Reset the "clear history" flag after the page has loaded again
if st.session_state["clear_history_pressed"]:
    st.session_state["clear_history_pressed"] = False
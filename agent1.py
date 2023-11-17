from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import os
import streamlit as st
from const import openai_key

os.environ["OPENAI_API_KEY"] = openai_key
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def app():
    st.title("Query Page")
    st.write("Ask your CSV 📈")
  
    csv_file = st.file_uploader("Upload a CSV file", type="csv")
  
    if csv_file is not None:

        agent = create_csv_agent(
            OpenAI(temperature=0), csv_file, verbose=True)

        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.chat_input("What is up?") if csv_file else ""

        if query:
          st.chat_message("user").markdown(query)
          st.session_state.messages.append({"role": "user", "content": query})
          
        ans = agent.run(query)

        with st.chat_message("assistant"):
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

if __name__ == '__main__':
    app()

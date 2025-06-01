from langchain_helper import get_free_shot_db_chain
import streamlit as st

st.title("QABot - Answers to Your Questions")
st.write("Ask questions about the Atliq T-Shirts database!")

question = st.text_input("Enter your question:")
if question:
    chain = get_free_shot_db_chain()
    answer = chain({"Question": question})
    st.header("Answer:")
    st.write(answer.get("Answer", "No answer found."))
    
    
    
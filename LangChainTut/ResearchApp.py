import os
import streamlit as st
import pickle
import time
import langchain
import langchain_community
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from secret_key import API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv() # Load environment variables from .env file

os.environ['GEMINI_API_KEY'] = API_KEY

# Intialize LLM 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,
    google_api_key= API_KEY #os.environ.get("GEMINI_API_KEY")
)
# create embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=API_KEY #os.environ.get("GEMINI_API_KEY"
    )
st.title("LangChain Research App")
st.write("This app allows you to search for information from a list of URLs and get answers with sources.")

st.sidebar.title("Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}", key=f"url_{i}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Load URLs", key="load_urls")
main_placeholder = st.empty()

file_path = "C:/Users/aumpa/OneDrive/Documents/GitHub/LangChain/LangChainTut/vector_index"

if process_url_clicked:
    # loading the URLs

    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    main_placeholder.text("Loading URLs... Please wait.")
    # splitting the text
    text_splitter = RecursiveCharacterTextSplitter(
                    #separators=['\n\n', '\n', ''],
                    chunk_size=1000,
                    chunk_overlap=200,)
    docs = text_splitter.split_documents(data)
    main_placeholder.text("Splitting the text...")
    
    vectorindex_gemini = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Creating vector index...")
    # Save the vector index using FAISS's save_local method
    vectorindex_gemini.save_local(file_path)
    main_placeholder.text("Vector index saved! You can now ask questions.")

main_placeholder.text_input("Question: ")
question = main_placeholder.text_input("Ask a question about the articles:", key="question")
if question:
    if os.path.exists(file_path):
        try:
            # Load the vector store using FAISS.load_local (not pickle)
            vectorstore = FAISS.load_local(
                file_path, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            
            chain = RetrievalQAWithSourcesChain.from_llm(
                llm=llm, 
                retriever=vectorstore.as_retriever()
            )
            
            result = chain({"question": question}, return_only_outputs=True)
            
            # Display results
            st.header("Answer:")
            st.write(result['answer'])
            
            if 'sources' in result:
                st.header("Sources:")
                st.write(result['sources'])
                
        except Exception as e:
            st.error(f"Error loading vector store: {e}")
    else:
        st.warning("Please load URLs first to create the vector index.")
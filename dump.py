from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from dotenv import load_dotenv
import os
import logging
from src.prompt import *
from logger import logging


# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Retrieve Pinecone API Key from environment variables
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in the environment variables.")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Download embeddings
embeddings = download_hugging_face_embeddings()

# Define Pinecone index name
index_name = "medicalchatbot"

# Initialize the Pinecone vector store
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Define the prompt template
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Initialize the LLM
llm = CTransformers(
    model="Model/llama-2-7b-chat.ggmlv3.q4_0.bin",
    model_type="llama",
    config={'max_new_tokens': 512, 'temperature': 0.8}
)

# Initialize the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs
)

# Define the main route
@app.route("/")
def index():
    return render_template('chat.html')

# Define the chat route
@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "")
        if not msg:
            return jsonify({"error": "No message provided"}), 400  # Bad Request
        
        logging.info(f"Input: {msg}")
        #response = qa.invoke({"query": msg})
        response=qa({"query": msg})

        logging.info(f"Response: {response['result']}")
        return str(response['result'])
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred during processing"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

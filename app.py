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
from medicalbot.pipeline.prediction_pipeline import MedicalbotModel



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


# medical_model_load = MedicalbotModel()
# llama_model = medical_model_load.predict()


def load_first_model_file_from_folder(folder_path: str):
    """
    This function loads the first model file from the specified folder.

    Parameters:
    - folder_path (str): Path to the folder containing saved models.

    Returns:
    - The model file name (str) if a model file is found.
    """
    try:
        # List files in the directory
        model_files = os.listdir(folder_path)

        # Check if folder is empty
        if not model_files:
            logging.info(f"The folder {folder_path} is empty.")
            return None
        else:
            # Return the first file in the folder
            logging.info(f"Using the first model file from folder: {model_files[0]}")
            return model_files[0]

    except Exception as e:
        logging.error(f"Error accessing folder {folder_path}: {str(e)}")
        raise e

<<<<<<< HEAD
=======

# Specify the folder path
save_model_folder = "C:\\Users\\pramod\\Desktop\\INURON\\Internship3\\Gen-AI-Medical_Chatbot\\savemodel"  # Change this to the actual folder path

# Check if the folder exists, and create it if it does not
if not os.path.exists(save_model_folder):
    os.makedirs(save_model_folder)
    print(f"Folder created: {save_model_folder}")
else:
    print(f"Folder already exists: {save_model_folder}")

>>>>>>> new-branch
# Folder where the saved models are stored
save_model_folder = "C:\\Users\\pramod\Desktop\\INURON\\Internship3\\Gen-AI-Medical_Chatbot\\savemodel"  # Change this to the actual folder path

try:
    logging.info("Entered the process of checking the save model folder.")

    # Check if the save model folder is empty or not
    model_file = load_first_model_file_from_folder(save_model_folder)

    if model_file is None:
        logging.info("Save model folder is empty. Proceeding to load the LLaMA model.")

        # Initialize the class responsible for loading the LLaMA model
        medical_model_load = MedicalbotModel()

        # Load the LLaMA model
        full_model_path = medical_model_load.load_llama_model()
        
        logging.info(f"LLaMA model loaded successfully.{full_model_path}")
        print(full_model_path)
    else:
        # Use the first file in the folder as the model
        llama_model = model_file
        full_model_path = os.path.join(save_model_folder, llama_model)
        logging.info(f"LLaMA model loaded from saved model folder: {llama_model}")

except Exception as e:
    logging.error(f"Error loading the LLaMA model: {str(e)}")
    raise ValueError("Could not load the LLaMA model.")





# Initialize the LLM
llm = CTransformers(
    model= full_model_path,
    model_type="llama",
    config={'max_new_tokens': 512, 'temperature': 0.8}
)
logging.info(f"CTransformers Done")
print("CTransformers Done")

# Initialize the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs
)

logging.info(f"RetrievalQA Done")
print("RetrievalQA Done")
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

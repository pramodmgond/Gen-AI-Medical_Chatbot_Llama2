
import logging
from src.prompt import *
from logger import logging
from medicalbot.pipeline.prediction_pipeline import MedicalbotModel




# medical_model_load = MedicalbotModel()
# llama_model = medical_model_load.predict()

try:
    logging.error(f"Entered load Llama model: ")

    medical_model_load = MedicalbotModel()
    
    llama_model = medical_model_load.load_llama_model()  # Adjust this method accordingly
except Exception as e:
    logging.error(f"Error loading the Llama model: {str(e)}")
    raise ValueError("Could not load the Llama model.")


import sys

from sklearn.pipeline import Pipeline

from medicalbot.exception import MedicalException
from logger import logging


class MedicalModel:
    def __init__(self, trained_model_object: object):
        """
        Initializes the MedicalModel class with a trained model object.
        
        :param trained_model_object: Input Object of trained model (e.g., a scikit-learn, TensorFlow, or PyTorch model)
        """
        self.trained_model_object = trained_model_object
    
    def predict(self, input_data):
        """
        Make predictions using the trained model.
        
        :param input_data: Data on which prediction needs to be performed (e.g., pandas DataFrame or numpy array)
        :return: The predictions made by the trained model
        """
        try:
            # Assuming the trained_model_object has a 'predict' method
            predictions = self.trained_model_object.predict(input_data)
            
            return predictions
        except AttributeError:
            raise Exception("The trained model object does not have a 'predict' method.")
        except Exception as e:
            raise Exception(f"Error during prediction: {str(e)}")

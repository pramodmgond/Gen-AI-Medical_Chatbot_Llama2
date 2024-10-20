from medicalbot.constants import is_model_accepted
from logger import logging
from medicalbot.exception import MedicalException
from medicalbot.components.model_pusher import ModelPusher
import sys
from medicalbot.constants import MODEL_TRAINER_MODEL_CONFIG_FILE_PATH, MODEL_BUCKET_NAME, MODEL_FILE_NAME
from medicalbot.entity.artifact_entity import ModelPusherArtifact 

from medicalbot.entity.config_entity import (
                                              ModelPusherConfig
) 
                                  

class TrainPipeline:
    def __init__(self):

        self.model_pusher_config = ModelPusherConfig()

    def start_model_pusher(self, local_model_path: str):
        """
        This method of the TrainPipeline class is responsible for starting model pushing.
        :param local_model_path: The local file path to the model that needs to be uploaded.
        :return: model_pusher_artifact: An artifact indicating the result of the model push.
        """
        try:
            # Create ModelPusher object with bucket and model file details
            model_pusher = ModelPusher(MODEL_BUCKET_NAME, MODEL_FILE_NAME)
            
            # Initiate model push to S3
            model_pusher_artifact = model_pusher.initiate_model_pusher(local_model_path)
            
            return model_pusher_artifact
        except Exception as e:
            raise MedicalException(e, sys)
            

    def run_pipeline(self) -> None:
        """
        This method of the TrainPipeline class is responsible for running the complete pipeline.
        :param local_model_path: The local file path to the LLM model that needs to be uploaded.
        """
        local_model_path = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
        
        try:
            # Check if the model is accepted before pushing to S3
            if not is_model_accepted:
                logging.info("Model not accepted for deployment.")
                return None
            
            # Push the model to S3 using the model pusher
            model_pusher_artifact = self.start_model_pusher(local_model_path)

            # Log successful upload or further actions if needed
            logging.info(f"Model uploaded successfully: {model_pusher_artifact}")
            
        except Exception as e:
            raise MedicalException(e, sys)

import sys
from cloud_storage.aws_storage import SimpleStorageService
from medicalbot.exception import MedicalException
from logger import logging
from medicalbot.entity.s3_estimator import MedicalEstimator
from medicalbot.constants import MODEL_TRAINER_MODEL_CONFIG_FILE_PATH, MODEL_BUCKET_NAME, MODEL_FILE_NAME
from medicalbot.entity.artifact_entity import ModelPusherArtifact

class ModelPusher:
    def __init__(self, model_bucket_name: str, model_file_name: str):
        """
        Initialize ModelPusher with the necessary S3 configuration.
        
        :param model_bucket_name: S3 bucket name where the model will be uploaded.
        :param model_file_name: Path (key) in S3 where the model will be stored.
        """
        self.s3 = SimpleStorageService()
        self.medical_estimator = MedicalEstimator(bucket_name=model_bucket_name, model_path=model_file_name)

    def initiate_model_pusher(self, local_model_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH) -> None:
        """
        Initiates the model pusher process to upload the model to S3.
        
        :param local_model_path: The local file path of the model to upload.
        :return: None
        :raises MedicalException: If there is an error during model upload.
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            logging.info(f"Uploading model from {local_model_path} to S3 bucket: {MODEL_BUCKET_NAME}")

            # Upload the model file to the S3 bucket using MedicalEstimator
            self.medical_estimator.save_model(from_file=local_model_path)

            logging.info(f"Successfully uploaded model from {local_model_path} to S3.")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            
            model_pusher_artifact = ModelPusherArtifact(local_model_path)

            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")
            
            return model_pusher_artifact
        except Exception as e:
            logging.error(f"Failed to upload model to S3: {e}")
            raise MedicalException(e, sys) from e

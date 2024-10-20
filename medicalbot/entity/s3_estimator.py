from cloud_storage.aws_storage import SimpleStorageService
from medicalbot.exception import MedicalException
from medicalbot.entity.estimator import MedicalModel
import sys

import sys
from cloud_storage.aws_storage import SimpleStorageService
from medicalbot.exception import MedicalException
from logger import logging
from pandas import DataFrame


class MedicalEstimator:
    """
    This class is used to save and retrieve the LLma2 model in an S3 bucket and perform predictions.
    """

    def __init__(self, bucket_name: str, model_path: str):
        """
        :param bucket_name: Name of your S3 bucket where the model is stored.
        :param model_path: Path (key) to the model file in the S3 bucket.
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: MedicalModel = None  # Corrected syntax

    def save_model(self, from_file: str, remove: bool = False) -> None:
        """
        Save the model to the specified model path in the S3 bucket.
        
        :param from_file: The local file path of the model to upload.
        :param remove: If True, the local model file will be deleted after uploading to S3.
        :return: None
        """
        try:
            logging.info(f"Uploading model from {from_file} to S3 bucket: {self.bucket_name}")

            # Upload the model file to the S3 bucket
            self.s3.upload_file(
                from_filename=from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove  # Flag to remove the local file after upload
            )

            logging.info(f"Successfully uploaded model to {self.model_path} in bucket {self.bucket_name}.")

            # Optionally, log if the local file is removed
            if remove:
                logging.info(f"Local file {from_file} removed after upload.")

        except Exception as e:
            logging.error(f"Failed to upload model from {from_file} to S3 bucket: {e}")
            raise MedicalException(e, sys)


    def is_model_present(self,model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except MedicalException as e:
            print(e)
            return False

    def load_model_llm(self,)->MedicalModel:
        """
        Load the model from the model_path
        :return:
        """

        #return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)
        return self.s3.download_model_from_s3(s3_bucket=self.bucket_name, s3_key= self.model_path)

    def load_model_to_predict(self):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                logging.info(f"Loading model from S3: bucket={self.bucket_name}, model_path={self.model_path}")

                self.loaded_model = self.load_model_llm()

                logging.info("Model loaded successfully")

            return self.loaded_model
        except Exception as e:
            raise MedicalException(e, sys)
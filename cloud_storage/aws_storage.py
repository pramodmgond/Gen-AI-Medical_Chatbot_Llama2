import boto3
from configuration.aws_connection import S3Client
from io import StringIO
from typing import Union,List
import os,sys
from logger import logging
from mypy_boto3_s3.service_resource import Bucket
from medicalbot.exception import MedicalException 
from botocore.exceptions import ClientError
from pandas import DataFrame
from langchain_community.llms import CTransformers
from io import BytesIO
import tempfile





class SimpleStorageService:

    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

    def s3_key_path_available(self,bucket_name,s3_key)->bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            if len(file_objects) > 0:
                return True
            else:
                return False
        except Exception as e:
            raise MedicalException(e,sys)
            
    def read_object(self, file_object, decode=False):
        logging.info("Entering read_object method to read model data.")
        try:
            response = file_object.get()
            logging.debug(f"S3 Response: {response}")  # Log the full response for debugging
            
            # Read the body of the response
            model_data = response['Body'].read()  # This reads the binary data
            logging.debug(f"Read {len(model_data)} bytes from the model data.")
            
            if decode:
                return model_data.decode('utf-8')  # If you need to decode
                
            logging.info("Successfully read model data from S3.")
            return model_data
        except Exception as e:
            logging.error(f"Error reading object from S3: {str(e)}")
            return None
        finally:
            logging.info("Exited the read_object method of S3Operations class")

    def get_file_object( self, filename: str, bucket_name: str) -> Union[List[object], object]:
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from bucket_name bucket based on filename

        Output      :   list of objects or object is returned based on filename
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the get_file_object method of S3Operations class")

        try:
            bucket = self.get_bucket(bucket_name)

            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(file_objects)
            logging.info("Exited the get_file_object method of S3Operations class")

            return file_objs

        except Exception as e:
            raise MedicalException(e, sys) from e

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        """
        Method Name :   load_model
        Description :   This method loads the model_name model from bucket_name bucket and saves it 
                        to the 'savemodel' folder, then loads it using CTransformers.

        Output      :   The loaded model object
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.4
        Revisions   :   Saving model directly with the same name as from S3.
        """
        logging.info("Entered the load_model method of SimpleStorageService class")

        try:
            # Determine the model file path in S3
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )
            model_file = func()
            logging.debug(f"Determined model file path: {model_file}")
            
            # Retrieve the file object from S3
            file_object = self.get_file_object(model_file, bucket_name)
            logging.info("File object retrieved successfully: %s", file_object)

            # Read the binary content directly from the file object
            logging.info("Entering read_object method to read model data.")
            model_data = self.read_object(file_object, decode=False)

            if model_data is None:
                logging.error("Model data is None after reading from S3.")
                raise MedicalException("Model data could not be read from S3.", sys)

            logging.info("Successfully read model data from S3.")
            
            # Get the current working directory and define the 'savemodel' folder
            current_directory = os.getcwd()
            save_model_folder = os.path.join(current_directory, "savemodel")

            # Create the folder if it doesn't exist
            if not os.path.exists(save_model_folder):
                os.makedirs(save_model_folder)
                logging.info(f"Created directory: {save_model_folder}")

            # Save the model data in the 'savemodel' folder using the original model name
            model_save_path = os.path.join(save_model_folder, model_name)

            # Save the model data to the 'savemodel' folder with the original file name
            with open(model_save_path, "wb") as model_file:
                model_file.write(model_data)

            logging.info(f"Model saved at: {model_save_path}")

            # Load the model using CTransformers with the saved file path
            logging.info("Attempting to load the model using CTransformers.")
            model = CTransformers(model=model_save_path)
            logging.info("Model loaded successfully.")

            logging.info("Exited the load_model method of SimpleStorageService class")
            return model

        except                                                                                        Exception as e:
            logging.error("Error in load_model: %s", e, exc_info=True)
            raise MedicalException(e, sys) from e


    def download_model_from_s3(self, s3_bucket, s3_key):
        """Downloads a model from an S3 bucket and saves it locally with its original name.
        
        Args:
            s3_bucket: The name of the S3 bucket.
            s3_key: The S3 key of the model file (including its name).
        """
        # Create an S3 client
        s3 = boto3.client('s3')
        logging.info(f"connection to s3 bucket done successfully")

        # Specify the local directory
        local_directory = "savemodel"

        # Ensure the local directory exists; create it if it doesn't
        os.makedirs(local_directory, exist_ok=True)

        # Extract the filename from the S3 key
        file_name = os.path.basename(s3_key)

        # Construct the full local path
        local_file_path = os.path.join(local_directory, file_name)
        logging.info(f"local folder path created : {local_file_path}")

        # Download the model from S3 directly
        s3.download_file(s3_bucket, s3_key, local_file_path)
        logging.info(f"Model downloaded and saved as: {local_file_path}")

        print(f"Model downloaded and saved as: {local_file_path}")
        
        return local_file_path


    def upload_file(self, from_filename: str, to_filename: str,  bucket_name: str,  remove: bool = True):
        """
        Method Name :   upload_file
        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename

        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the upload_file method of S3Operations class")

        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )

            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)

                logging.info(f"Remove is set to {remove}, deleted the file")

            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")

            logging.info("Exited the upload_file method of S3Operations class")

        except Exception as e:
            raise MedicalException(e, sys) from e
   
    
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Method Name :   create_folder
        Description :   This method creates a folder_name folder in bucket_name bucket

        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the create_folder method of S3Operations class")

        try:
            self.s3_resource.Object(bucket_name, folder_name).load()

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            else:
                pass
            logging.info("Exited the create_folder method of S3Operations class")
    
    
    
    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket object based on the bucket_name

        Output      :   Bucket object is returned based on the bucket name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the get_bucket method of S3Operations class")

        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of S3Operations class")
            return bucket
        except Exception as e:
            raise MedicalException(e, sys) from e

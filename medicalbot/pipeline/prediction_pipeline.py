import os
import sys

import numpy as np
import pandas as pd
from medicalbot.entity.config_entity import MedicalPredictorConfig
from medicalbot.entity.s3_estimator import MedicalEstimator
from medicalbot.exception import MedicalException
from logger import logging
from pandas import DataFrame


class MedicalbotModel:
    def __init__(self,prediction_pipeline_config: MedicalPredictorConfig = MedicalPredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MedicalException(e, sys)

    def load_llama_model(self) -> str:
        """
        This is the method of Medicalbot
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered load_llama_model method of MedicalbotModel class")
            model = MedicalEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.load_model_to_predict()
            
            return result
        
        except Exception as e:
            raise MedicalException(e, sys)
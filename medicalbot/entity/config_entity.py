from medicalbot.constants import *
from dataclasses import dataclass

    
    
@dataclass
class ModelPusherConfig:
    local_model_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    
@dataclass
class MedicalPredictorConfig:
    model_file_path: str = MODEL_FILE_NAME
    model_bucket_name: str = MODEL_BUCKET_NAME

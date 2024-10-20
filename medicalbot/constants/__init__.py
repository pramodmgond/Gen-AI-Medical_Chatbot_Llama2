import os
from datetime import date
from urllib.parse import quote_plus



MODEL_FILE_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"

is_model_accepted = True

"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "Model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "llama-2-7b-chat.ggmlv3.q4_0.bin"
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join(MODEL_TRAINER_DIR_NAME, MODEL_TRAINER_TRAINED_MODEL_NAME)


AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"

MODEL_BUCKET_NAME = "llma2-model"
MODEL_PUSHER_S3_KEY = "model-registry"


""" prediction pipe line 
"""
APP_HOST = "0.0.0.0"
APP_PORT = 8080
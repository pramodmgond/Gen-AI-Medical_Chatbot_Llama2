import logging
import os
from from_root import from_root
from datetime import datetime

# Set up log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the log directory name
log_dir = 'logs'

root_path = r"C:\Users\pramod\Desktop\INURON\Internship3\Gen-AI-Medical_Chatbot"
# Create the full path for the log directory within the project root
logs_dir_path = os.path.join(root_path, log_dir)
print(f"Log directory path: {logs_dir_path}")  # Debugging statement to confirm the directory path

# Create the full path for the log file within the logs directory
log_file_path = os.path.join(logs_dir_path, LOG_FILE)
print(f"Log file path: {log_file_path}")  # Debugging statement to confirm the log file path

# Ensure the log directory exists (creates the directory if it doesn't exist)
os.makedirs(logs_dir_path, exist_ok=True)
print(f"Log directory created: {logs_dir_path}")  # Confirming directory creation

# Configure the logging system to write log messages to the specified file
logging.basicConfig(
    filename=log_file_path,  # File path for the log file
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",  # Log message format
    level=logging.DEBUG,  # Log level (captures DEBUG and higher level messages)
)

# Test logging to verify setup
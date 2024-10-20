import os
import sys

def error_message_detail(error, error_detail: sys):
    exc_type, exc_obj, exc_tb = error_detail.exc_info()
    
    # Safeguard if traceback (exc_tb) is None
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in script [{file_name}] at line [{line_number}] - {str(error)}"
    else:
        # If traceback is None, return a basic error message
        error_message = f"Error: {str(error)}"

    return error_message

class MedicalException(Exception):
    def __init__(self, error_message, error_detail: sys):
        """
        Custom exception class to capture error details such as file name and line number.
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message

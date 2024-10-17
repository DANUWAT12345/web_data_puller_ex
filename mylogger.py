import logging
import sys

def setup_logger(log_file_name):
    # Configure the logger to write to the file
    logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s - %(message)s')

    # Add a handler to also log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)

    # Redirect sys.stdout to both the log file and the console
    class DoubleOutput:
        def __init__(self, *outputs):
            self.outputs = outputs

        def write(self, text):
            for output in self.outputs:
                output.write(text)

        def flush(self):
            for output in self.outputs:
                output.flush()

    log_file = open(log_file_name, 'a')
    double_output = DoubleOutput(sys.stdout, log_file)
    sys.stdout = double_output

    return log_file, double_output.outputs[0]

def close_logger(log_file, original_stdout):
    # Properly close the log file and restore sys.stdout
    log_file.close()
    sys.stdout = original_stdout

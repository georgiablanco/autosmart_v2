import time
import logging

def createFileLogger(log_file_name):

        logger = logging.Logger('')
        logger.setLevel(logging.DEBUG)
        fileh = logging.FileHandler(log_file_name,  mode='w')
        fileh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(process)d - %(processName)s - %(thread)d - %(levelname)s - %(message)s')
        fileh.setFormatter(formatter)
        logger.addHandler(fileh)
        return logger


      # logger = logging.basicConfig(filename=log_file_name, 
        # 							format='%(asctime)s - %(process)d - %(levelname)s - %(message)s',
        # 							level=logging.DEBUG)
        # return logger
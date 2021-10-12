import logging
from datetime import datetime
import json
import sys

class logger_class():
    """docstring for setup_logger"""
    def __init__(self,root_path):
        self.root_path = root_path
        self.Months = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
        self.currentMonth = datetime.now().month
        self.currentYear = datetime.now().year
        # Get from the config_file.json the path where the script will save the logging
        self.logs_path, self.logs_level_name = self.get_logs_parameters()
        self.logger = self.logger_setup() 

    def get_logs_parameters(self):
        try:
            with open(self.root_path+"/config_file.json","r") as jsonfile:
                ConfigData = json.load(jsonfile)
                logs_path = ConfigData["generic_config"]["logs_path"]
                logs_level = ConfigData["generic_config"]["logs_level"]
        except Exception as e:
            print("There was an error trying to open the config JSON file or getting the logs_path. %s. %s" %(sys.exc_info()[0],e))
            raise
        return logs_path, logs_level


    def get_logs_level_value(self):
        if self.logs_level_name == "DEBUG":
            return logging.DEBUG
        elif self.logs_level_name == "INFO":
            return logging.INFO
        elif self.logs_level_name == "WARNING":
            return logging.WARNING
        elif self.logs_level_name == "ERROR":
            return logging.ERROR
        else:
            print("wrong log level name")
            raise


    def logger_setup(self):
        #---------------- Instantiate a logger object -------------------------------
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        #---------------- our first handler is a console handler --------------------
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.get_logs_level_value())
        console_handler_format = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
        console_handler.setFormatter(logging.Formatter(console_handler_format))
        logger.addHandler(console_handler)
        #---------------- the second handler is a file handler ----------------------
        file_handler = logging.FileHandler(self.logs_path+"/Logs_%s_%s.log" %(self.Months[self.currentMonth],self.currentYear))
        file_handler.setLevel(self.get_logs_level_value())
        file_handler_format = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
        file_handler.setFormatter(logging.Formatter(file_handler_format))
        logger.addHandler(file_handler)
        #----------------------------------------------------------------------------
        return logger
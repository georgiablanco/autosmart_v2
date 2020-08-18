## Author: Kud01
## Date: 11/07/2018

from  ConfigParser import SafeConfigParser
import logging

config_file="config/config.ini"

logger = logging.getLogger('autosmart')

class configurators:
    def __init__(self):
        try:
            self.config = SafeConfigParser()
            self.config.read(config_file)
        except Exception as err:
            logger.error("Error opening config file:" + config_file)
        logger.debug(self.config.sections())

    def get_config(self,section,attribute):
        if(self.config.has_option(section,attribute)):
            logger.info("Successfully retrieved: [%s][%s]",section,attribute)
            return (self.config.get(section,attribute))
        else:
            logger.error("config items not found: [%s][%s]",section,attribute)
            return None




import logging
from decouple import config
#
#
logging.basicConfig(filename=config('ERROR_LOG_PATH'), level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S%p')
logger = logging.getLogger(__name__)
def get_curl_logger():
    logger = logging.getLogger('curl_log')
    logger.setLevel(logging.ERROR)
    fileHandler = logging.FileHandler("curl_log.log", mode='a')
    fileHandler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S%p')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger
   # def testLog(self):
   #     #logger = logging.getLogger('demologger')
   #     logger = logging.getLogger(LoggerDemoConsole.__name__)
   #     logger.setLevel(logging.INFO)
   #     fileHandler = logging.FileHandler("curl.log",mode='a')
   #     fileHandler.setLevel(logging.INFO)
   #     formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
   #     fileHandler.setFormatter(formatter)
   #     logger.addHandler(fileHandler)
   #     logger.ERROR('ERROR message')
   #     logger.info('info message')
   #     logger.warn('warn message')
   #     logger.error('error message')
   #     logger.critical('critical message')

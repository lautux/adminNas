#! /usr/bin/python3

import config
import subprocess
import traceback
from classes.logger import Logger
from datetime import datetime

class Rclone:
    """
    Class to manage sync between nas and pcloud
    """
    logger = None

    def __init__(self, logger:Logger=None):
        """
        Constructor

        Parameters:
        logger (Logger): Logger object 
        """
        self.logger = logger


    def __send(self, localDir:str, remoteDir:str) -> bool:
        try:
            self.logger.debug(f"Rclone.send")
            status = False
            currentDatetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            logFileName = f"rclone_{currentDatetime}.log"
            logFilePath = f"{config.NAS2PCLOUD_LOG_DIR}{logFileName}"
            cmd = [
                "rclone",
                "copy",
                *config.RCLONE_OPTIONS,
                f"--log-file={logFilePath}",
                localDir,
                f"pcloud:{remoteDir}"
            ]
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.logger.info(f"stdout : {result.stdout}")
            self.logger.info(f"stderr : {result.stderr}")
            status = (result.returncode == 0)
            self.logger.info("Command executed successfully")
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return status


    def sendPhotos(self) -> bool:
        return self.__send(config.NAS_PHOTOS_PATH, config.PCLOUD_PHOTOS_PATH)

    def sendData(self) -> bool:
        return self.__send(config.NAS_DATA_PATH, config.PCLOUD_DATA_PATH)
    
    def sendTest(self) -> bool:
        return self.__send(config.NAS_TEST_PATH, config.PCLOUD_TEST_PATH)


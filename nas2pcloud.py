#! /usr/bin/python3

###############################################################################
# Import classes
###############################################################################
#import logging
import config
import subprocess
from classes.logger import Logger
from datetime import datetime

class Nas2Pcloud:
    """
    Class to manage sync between nas and pcloud
    """
    logger = None

    def __init__(self, logger=None):
        """
        Constructor

        Parameters:
        logger (Logger): Logger object 
        """
        self.logger = logger


    def sendPhotos(self) -> bool:
        try:
            self.logger.debug(f"Nas2Pcloud.sendPhotos")
            status = False
            currentDatetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            logFileName = f"rclone_photo_{currentDatetime}.log"
            logFilePath = f"{config.NAS2PCLOUD_LOG_DIR}{logFileName}"
            cmd = f"rclone copy --dry-run --verbose --progress --log-file={logFilePath} {config.NAS_PHOTOS_PATH} pcloud:{config.PCLOUD_PHOTOS_PATH}"
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            status = (result.returncode == 0)
        except Exception as e:
            status = False
            self.logger.error(f"Error in Nas2Pcloud.sendPhotos : {e.stderr}")
        finally:
            return status


    
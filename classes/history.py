#! /usr/bin/python3

import subprocess
import traceback
import config

class History:
    """
    Class to manage history data
    """
    logger       = None

    def __init__(self, logger=None):
        """
        Constructor

        Parameters:
        mountPoints (array): Linux mount points. Ex: /mnt/raid4to.
        """
        self.logger = logger

    def getDfGraph(self) -> bool:
        try:
            self.logger.debug(f"Df.getGlobalStatus - DEBUT")
            status = True
            for mnt in self.mountPoints:
                if not self.getDfStatus(mnt):
                    status = False
                    break
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getGlobalStatus - FIN")
            return status

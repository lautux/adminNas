#! /usr/bin/python3

import sys

class Param:
    """
    Class to manage script params
    """
    argv = []

    def __init__(self, argv, logger=None):
        """
        Constructor
        """
        self.argv = argv
        self.logger = logger

    def getGlobalStatus(self) -> bool:
        try:
            status = False
            cpu = self.getCpuPercent()
            status = (cpu <= 80)
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return status


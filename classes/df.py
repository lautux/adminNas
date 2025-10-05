#! /usr/bin/python3

import subprocess
import traceback
import config

class Df:
    """
    Class to get df data
    """
    mountPoints = []
    checkCommand = ""
    logger       = None

    def __init__(self, mountPoints, logger=None):
        """
        Constructor

        Parameters:
        mountPoints (array): Linux mount points. Ex: /mnt/raid4to.
        """
        self.mountPoints = mountPoints
        self.logger = logger
        # df -x tmpfs -x devtmpfs -x efivarfs -k /mnt/raid4to | awk 'NR>1 {gsub("%", "", $5); print $5}'
        self.checkCommand = ["sudo", "df", "-h"]

    def __getCheckCommand(self, mountPoint:str) -> str:
        try:
            self.logger.debug(f"Df.__getCheckCommand")
            tabCmd = self.checkCommand.copy()
            tabCmd.append(mountPoint)
        except Exception as e:
            tabCmd = []
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return tabCmd

    def getGlobalStatus(self) -> bool:
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

    def getGlobalDetails(self, badOnly:bool=True) -> bool:
        try:
            self.logger.debug(f"Df.getGlobalDetail")
            details = ""
            for mnt in self.mountPoints:
                details += f"Df status of {mnt} : {'OK' if self.getDfStatus(mnt) else 'KO'} ({self.getDfPercent(mnt)}%)\n"
                if (not badOnly) or (not self.getDfStatus(mnt)):
                    details += f"\t{' '.join(self.__getCheckCommand(mnt))}\n"
                    details += f"\t{self.getDfDetail(mnt)}\n"
        except Exception as e:
            details = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return details

    def getDfStatus(self, mnt) -> bool:
        try:
            self.logger.debug(f"Df.getDfStatus - DEBUT")
            percent = self.getDfPercent(mnt)
            self.logger.debug(f"Df.getDfStatus - percent = {percent}")
            status = (percent <= config.DF_THREATHOLD)
            self.logger.debug(f"Df.getDfStatus - status = {status}")
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getDfStatus - FIN")
            return status

    def getDfPercent(self, mnt) -> int:
        try:
            self.logger.debug(f"Df.getDfPercent - DEBUT")
            percent = 100
            for line in self.getDfDetail(mnt).splitlines()[1:]:
                percent = int(line.split()[4].rstrip('%'))
        except Exception as e:
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getDfPercent - FIN")
            return percent

    def getDfDetail(self, mnt) -> str:
        try:
            self.logger.debug(f"Df.getDfDetail - DEBUT")
            dfDetail = None
            cmd = self.__getCheckCommand(mnt)
            self.logger.debug(f"cmd : {cmd}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            dfDetail = result.stdout
            self.logger.debug(f"dfDetail : {dfDetail}")
        except Exception as e:
            dfDetail = None
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getDfDetail - FIN")
            return dfDetail


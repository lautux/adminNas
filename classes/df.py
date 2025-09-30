#! /usr/bin/python3

import subprocess
import traceback
import config
import re

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
                details += f"Df status of {mnt} : {"OK" if self.getDfStatus(mnt) else "KO"}\n"
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
            status = False
            percent = 100
            for line in self.getDfDetail(mnt).splitlines():
                # Vérifier si le % d'utilisation est > au seuil
                self.logger.debug(f"line : {line}")
                if re.match(r'\s+' + mnt + r'$', line):
                    self.logger.debug(f"line match :-)")
                    percent = line.split()[4].rstrip('%')
                else:
                    self.logger.debug(f"line not match :-(")
            self.logger.debug(f"percent : {percent}")
            status = (percent <= config.DF_THREATHOLD)
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getDfStatus - FIN")
            return status

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


#! /usr/bin/python3

import subprocess
import traceback

class Raid:
    """
    Class to manage raid volume
    """
    raidDevices  = []
    checkCommand = ""
    logger       = None

    def __init__(self, devices, logger=None):
        """
        Constructor

        Parameters:
        devices (array): Linux devices corresponding to raid array. Ex: /dev/md0.
        """
        self.raidDevices = devices
        self.logger = logger
        self.checkCommand = ["sudo", "mdadm", "--detail"]
        self.logger.debug(f"Raid.__init__")

    def __getCheckCommand(self, device:str) -> str:
        try:
            self.logger.debug(f"Raid.__getCheckCommand")
            tabCmd = self.checkCommand.copy()
            tabCmd.append(device)
        except Exception as e:
            tabCmd = []
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return tabCmd

    def getGlobalStatus(self) -> bool:
        try:
            self.logger.debug(f"Raid.getGlobalStatus")
            status = True
            for dev in self.raidDevices:
                if not self.getRaidStatus(dev):
                    status = False
                    break
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return status
    
    def getGlobalDetails(self, badOnly:bool=True) -> bool:
        try:
            self.logger.debug(f"Raid.getGlobalDetail")
            details = ""
            for dev in self.raidDevices:
                details += f"Raid array {dev} : {"OK" if self.getRaidStatus(dev) else "KO"}\n"
                if (not badOnly) or (not self.getRaidStatus(dev)):
                    details += f"\t{' '.join(self.__getCheckCommand(dev))}\n"
                    details += f"\t{self.getRaidDetail(dev)}\n"
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return details

    def getRaidStatus(self, device:str) -> bool:
        try:
            self.logger.debug(f"Raid.getRaidStatus")
            status = False
            cmd = self.__getCheckCommand(device)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            raidDetail = result.stdout
            for line in raidDetail.splitlines():
                if "State :" in line:
                    state = line.split(":")[1].strip()
            status = (state == "clean")
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return status

    def getRaidDetail(self, device:str) -> str:
        try:
            self.logger.debug(f"Raid.getRaidDetail")
            raidDetail = ""
            cmd = self.checkCommand.copy()
            cmd.append(device)
            self.logger.debug(f"cmd : {cmd}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            raidDetail = result.stdout
        except Exception as e:
            raidDetail = ""
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            return raidDetail


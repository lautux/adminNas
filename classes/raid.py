#! /usr/bin/python3

import subprocess

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
            self.logger.error(f"Error in getGlobalStatus : {e.stderr}")
        finally:
            return status

    def getRaidStatus(self, device) -> bool:
        try:
            self.logger.debug(f"Raid.getRaidStatus")
            status = False
            cmd = self.checkCommand.copy()
            cmd.append(device)
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
            self.logger.error(f"Error in getRaidStatus : {e.stderr}")
        finally:
            return status

    def getRaidDetail(self, device) -> str:
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
            self.logger.error(f"Error in getRaidDetail : {e.stderr}")
        finally:
            return raidDetail


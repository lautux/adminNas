#! /usr/bin/python3

import subprocess

class Smart:
    """
    Class to manage smart data for hdd
    """
    smartDevices = []
    checkCommand = ""
    logger       = None

    def __init__(self, devices, logger=None):
        """
        Constructor

        Parameters:
        devices (array): Linux devices corresponding to the hdd. Ex: /dev/sda.
        """
        self.smartDevices = devices
        self.logger = logger
        self.checkCommand = ["sudo", "smartctl", "-H"]

    def getGlobalStatus(self) -> bool:
        try:
            self.logger.debug(f"Smart.getGlobalStatus - DEBUT")
            status = True
            for dev in self.smartDevices:
                if not self.getSmartStatus(dev):
                    status = False
                    break
        except Exception as e:
            status = False
            self.logger.error(f"Error in getGlobalStatus : {e.stderr}")
        finally:
            self.logger.debug(f"Smart.getGlobalStatus - FIN")
            return status

    def getSmartStatus(self, device) -> bool:
        try:
            self.logger.debug(f"Smart.getSmartStatus - DEBUT")
            status = False
            state = None
            for line in self.getSmartDetail(device).splitlines():
                if "test result:" in line:
                    state = line.split(":")[1].strip()
            self.logger.debug(f"state : {state}")
            status = (state == "PASSED")
        except Exception as e:
            status = False
            self.logger.error(f"Error in getSmartStatus : {e.stderr}")
        finally:
            self.logger.debug(f"Smart.getSmartStatus - FIN")
            return status

    def getSmartDetail(self, device) -> str:
        try:
            self.logger.debug(f"Smart.getSmartDetail - DEBUT")
            smartDetail = None
            cmd = self.checkCommand.copy()
            cmd.append(device)
            self.logger.debug(f"Smart.getSmartDetail - cmd : {cmd}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            smartDetail = result.stdout
            self.logger.debug(f"smartDetail : {smartDetail}")
        except Exception as e:
            smartDetail = None
            self.logger.error(f"Error in getSmartDetail : {e}")
        finally:
            self.logger.debug(f"Smart.getSmartDetail - FIN")
            return smartDetail


#sudo smartctl -H /dev/sda 2>/dev/null | grep -E "SMART overall-health|SMART Health Status|test result" | grep -Eo "PASSED|OK|FAILED" | sed "s/OK/PASSED/"

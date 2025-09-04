#! /usr/bin/python3

import subprocess

class Smart:
    """
    Class to manage smart data for hdd
    """
    smartDevice  = ""
    smartDetail  = ""
    checkCommand = ""

    def __init__(self, dev):
        """
        Constructor

        Parameters:
        dev (str): Linux device corresponding to the hdd. Ex: /dev/sda.
        """
        self.smartDevice = dev
        self.checkCommand = ["sudo", "smartctl", "-H", self.smartDevice]

    def getGlobalStatus(self) -> bool:
        state = self.getSmartState()
        #print(state)
        return state == "PASSED"

    def getSmartState(self) -> str:
        try:
            state = "unknow"
            result = subprocess.run(
                self.checkCommand,
                capture_output=True,
                text=True,
                check=True
            )
            self.smartDetail = result.stdout
            #print(self.smartDetail)
            for line in self.smartDetail.splitlines():
                if "test result:" in line:
                    state = line.split(":")[1].strip()
            return state
        
        except subprocess.CalledProcessError as e:
            print(f"Error in getSmartState : {e.stderr}")
            return False

    def getSmartDetail(self) -> str:
        try:
            state = "unknow"
            result = subprocess.run(
                ["sudo", "smartctl", "-H", self.smartDevice],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        
        except subprocess.CalledProcessError as e:
            print(f"Error in getSmartDetail : {e.stderr}")
            return False


#sudo smartctl -H /dev/sda 2>/dev/null | grep -E "SMART overall-health|SMART Health Status|test result" | grep -Eo "PASSED|OK|FAILED" | sed "s/OK/PASSED/"

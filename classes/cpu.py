#! /usr/bin/python3

import subprocess
import psutil

class Cpu:
    """
    Class to manage CPU
    """
    cpuDetail  = ""
    checkCommand = ""

    def __init__(self):
        """
        Constructor
        """
        #self.checkCommand = ["sudo", "lscpu"] 
        #self.checkCommand = ["awk", "-v FS=\" \"", "/^cpu / {print 100*($2+$3+$4)/($2+$3+$4+$5)\"%\"}", "/proc/stat"]
        #awk -v FS=" " '/^cpu / {print 100*($2+$3+$4)/($2+$3+$4+$5)"%"}' /proc/stat

    def getGlobalStatus(self) -> bool:
        cpu = self.getCpuPercent()
        return cpu <= 80

    def getCpuPercent(self) -> float:
        try:
            return psutil.cpu_percent(interval=0.2)
        
        except subprocess.CalledProcessError as e:
            print(f"Error in getCpuPercent {e.stderr}")
            return False

    def getCpuDetail(self) -> str:
        try:
            state = "unknow"
            result = subprocess.run(
                self.checkCommand,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        
        except subprocess.CalledProcessError as e:
            print(f"Error in getCpuDetail : {e.stderr}")
            return False

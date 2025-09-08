#! /usr/bin/python3

import subprocess
import psutil

class Cpu:
    """
    Class to manage CPU
    """
    cpuDetail    = ""
    checkCommand = ""
    logger       = None

    def __init__(self, logger=None):
        """
        Constructor
        """
        #self.checkCommand = ["sudo", "lscpu"] 
        #self.checkCommand = ["awk", "-v FS=\" \"", "/^cpu / {print 100*($2+$3+$4)/($2+$3+$4+$5)\"%\"}", "/proc/stat"]
        #awk -v FS=" " '/^cpu / {print 100*($2+$3+$4)/($2+$3+$4+$5)"%"}' /proc/stat
        self.logger = logger

    def getGlobalStatus(self) -> bool:
        try:
            status = False
            cpu = self.getCpuPercent()
            status = (cpu <= 80)
        except Exception as e:
            status = False
            self.logger.error(f"Error in getGlobalStatus : {e.stderr}")
        finally:
            return status

    def getCpuPercent(self) -> float:
        try:
            cpu = None
            cpu = psutil.cpu_percent(interval=0.2)
        except Exception as e:
            cpu = None
            self.logger.error(f"Error in getCpuPercent : {e.stderr}")
        finally:
            return cpu

    def getCpuDetail(self) -> str:
        try:
            cpuDetail = None
            result = subprocess.run(
                self.checkCommand,
                capture_output=True,
                text=True,
                check=True
            )
            cpuDetail = result.stdout
        except Exception as e:
            cpuDetail = None
            self.logger.error(f"Error in getCpuDetail : {e.stderr}")
        finally:
            return cpuDetail

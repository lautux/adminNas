#! /usr/bin/python3

import subprocess

class Fail2ban:
    """
    Class to manage fail2ban
    """
    checkCommand     = ""
    bannedIpCommand  = ""
    fail2banStatus   = ""
    fail2banBannedIp = ""
    logger           = None

    def __init__(self, logger=None):
        """
        Constructor
        """
        self.logger = logger
        self.checkCommand = ["sudo", "systemctl", "status", "fail2ban"]
        self.bannedIpCommand = ["sudo", "fail2ban-client", "status", "sshd"]

    def getGlobalStatus(self) -> bool:
        try:
            status = True
            status = self.getFail2banStatus()
        except Exception as e:
            status = False
            self.logger.error(f"Error in getGlobalStatus : {e.stderr}")
        finally:
            return status
    
    def getFail2banStatus(self) -> bool:
        try:
            status = False
            state = "unknow"
            result = subprocess.run(
                self.checkCommand,
                capture_output=True,
                text=True,
                check=True
            )
            fail2banDetail = result.stdout
            #self.logger.debug(f"fail2banDetail : {fail2banDetail}")
            for line in fail2banDetail.splitlines():
                if "Active:" in line:
                    state = line.split(":")[1].strip().split(" ")[0].strip()
            status = (state == "active")
        except Exception as e:
            status = False
            self.logger.error(f"Error in getFail2banStatus : {e.stderr}")
        finally:
            return status

    def getBannedIp(self) -> str:
        try:
            ips = ""
            result = subprocess.run(
                self.bannedIpCommand,
                capture_output=True,
                text=True,
                check=True
            )
            self.fail2banBannedIp = result.stdout
            for line in self.fail2banBannedIp.splitlines():
                if "Banned IP list:" in line:
                    ips = line.split(":")[1].strip()
        except Exception as e:
            ips = ""
            self.logger.error(f"Error in getBannedIp : {e.stderr}")
        finally:
            return ips



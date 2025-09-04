#! /usr/bin/python3

import subprocess

class Fail2ban:
    """
    Class to manage fail2ban
    """
    checkCommand = ""
    bannedIpCommand = ""
    fail2banStatus = ""
    fail2banBannedIp = ""

    def __init__(self):
        """
        Constructor
        """
        self.checkCommand = ["sudo", "systemctl", "status", "fail2ban"]
        self.bannedIpCommand = ["sudo", "fail2ban-client", "status", "sshd"]

    def getGlobalStatus(self) -> bool:
        state = self.getFail2banStatus()
        #print(state)
        return state == "active"
    
    def getFail2banStatus(self) -> str:
        try:
            state = "unknow"
            result = subprocess.run(
                self.checkCommand,
                capture_output=True,
                text=True,
                check=True
            )
            self.fail2banStatus = result.stdout
            for line in self.fail2banStatus.splitlines():
                if "Active:" in line:
                    state = line.split(":")[1].strip().split(" ")[0].strip()
            return state
        
        except subprocess.CalledProcessError as e:
            print(f"Error in getFail2banStatus : {e.stderr}")
            return False

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
            return ips
        
        except subprocess.CalledProcessError as e:
            print(f"Error in getBannedIp : {e.stderr}")
            return False



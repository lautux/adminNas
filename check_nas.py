#! /usr/bin/python3

###############################################################################
# Import classes
###############################################################################
import logging
from classes.logger import Logger
from classes.raid import Raid
from classes.smart import Smart
from classes.fail2ban import Fail2ban
from classes.cpu import Cpu

log = Logger("/data/scripts/check_nas.log", logging.DEBUG)

print(f"{'-'*40}")
print(f"{'Status du NAS': ^{40}}")
print(f"{'-'*40}")


###############################################################################
# RAID devices
###############################################################################
raid = Raid(["/dev/md0",], log)
raid_globalStatus = raid.getGlobalStatus()
print(f"\n # Etat des RAID : {'OK' if raid_globalStatus else 'KO'}")
#print(f"getRaidDetail : {raid.getRaidDetail('/dev/md0')}")


###############################################################################
# SMART health
###############################################################################
print(f"\n # Santé des disques")
for devicePath in ("/dev/sda", "/dev/sdb", "/dev/nvme0"):
    smart = Smart(devicePath)
    smartGlobalStatus = smart.getGlobalStatus()
    #smartGlobalStatus = False
    if smartGlobalStatus:
        print(f"\t {devicePath} : OK")
    else:
        print(f"\t {devicePath} : KO")
        print(f"\t\t/!\\ Vérifier l'état de santé du disque : {' '.join(smart.checkCommand)}")


###############################################################################
# Fail2ban service status
###############################################################################
print(f"\n # Status de Fail2ban")
fail2ban = Fail2ban()
fail2banGlobalStatus = fail2ban.getGlobalStatus()
#fail2banGlobalStatus = False
if fail2banGlobalStatus:
    print(f"\t Service : OK")
else:
    print(f"\t Service : KO")
    print(f"\t\t/!\\ Vérifier l'état du service fail2ban : {' '.join(fail2ban.checkCommand)}")
fail2banBannedIp = fail2ban.getBannedIp()
print(f"\t IP bannies : {fail2banBannedIp}")


###############################################################################
# CPU status
###############################################################################
print(f"\n # Utilisation du CPU")
cpu = Cpu()
cpuGlobalStatus = cpu.getGlobalStatus()
#cpuGlobalStatus = False
if cpuGlobalStatus:
    print(f"\t Charge : OK")
else:
    print(f"\t Charge : KO")
    print(f"\t\t/!\\ Vérifier l'utilisation du CPU : {' '.join(cpu.checkCommand)}")


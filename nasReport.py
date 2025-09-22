#! /usr/bin/python3

###############################################################################
# Import classes
###############################################################################
import logging
import config
from classes.logger import Logger
from classes.raid import Raid
from classes.smart import Smart
from classes.fail2ban import Fail2ban
from classes.cpu import Cpu

log = Logger(f"{config.LOG_FILE_PATH}", logging.DEBUG)

print(f"{'-'*40}")
print(f"{'Status du NAS': ^{40}}")
print(f"{'-'*40}")


###############################################################################
# RAID devices
###############################################################################
raid = Raid(config.RAID_PATHS, log)
raid_globalStatus = raid.getGlobalStatus()
print(f"\n # Etat des RAID : {'OK' if raid_globalStatus else 'KO'}")
raid_globalStatus = False
if not raid_globalStatus:
    print(raid.getGlobalDetails(badOnly=False))


###############################################################################
# SMART health
###############################################################################
"""smart = Smart(config.HDD_PATHS, log)
smart_globalStatus = smart.getGlobalStatus()
print(f"\n # Santé des disques : {'OK' if smart_globalStatus else 'KO'}")
if not smart_globalStatus:
    print(f"\t/!\\ Vérifier l'état de santé du disque : {' '.join(smart.checkCommand)}")"""


###############################################################################
# Fail2ban service status
###############################################################################
"""fail2ban = Fail2ban(log)
fail2ban_globalStatus = fail2ban.getGlobalStatus()
print(f"\n # Status de Fail2ban : {'OK' if fail2ban_globalStatus else 'KO'}")
if not fail2ban_globalStatus:
    print(f"\t/!\\ Vérifier l'état du service fail2ban : {' '.join(fail2ban.checkCommand)}")"""


###############################################################################
# CPU status
###############################################################################
"""cpu = Cpu(log)
cpu_globalStatus = cpu.getGlobalStatus()
print(f"\n # Utilisation du CPU : {'OK' if cpu_globalStatus else 'KO'}")
#cpu_globalStatus = False
if not cpu_globalStatus:
    print(f"\t/!\\ Vérifier l'utilisation du CPU : {' '.join(cpu.checkCommand)}")"""


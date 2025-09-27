#! /usr/bin/python3

###############################################################################
# Import classes
###############################################################################
import logging
import config
import sys
import argparse
from classes.logger import Logger
from classes.raid import Raid
from classes.smart import Smart
from classes.fail2ban import Fail2ban
from classes.cpu import Cpu


def main():
    parser = argparse.ArgumentParser(description="Script d'analyse du NAS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-d", "--details", action="store_true", help="Show more details")
    args = parser.parse_args()
    loggingMode = config.LOGGING_MODE
    if(args.verbose):
        loggingMode = logging.DEBUG
        print(f"Activate DEBUG mode : {loggingMode}")
    log = Logger(f"{config.LOG_FILE_PATH}", loggingMode)

    ###############################################################################
    # Report header
    ###############################################################################
    print(f"{'-'*40}")
    print(f"{'Status du NAS': ^{40}}")
    print(f"{'-'*40}")


    ###############################################################################
    # RAID devices
    ###############################################################################
    raid = Raid(config.RAID_PATHS, log)
    raid_globalStatus = raid.getGlobalStatus()
    print(f"\n # Etat des RAID : {'OK' if raid_globalStatus else 'KO'}")
    if not raid_globalStatus or args.details:
        print(raid.getGlobalDetails())


    ###############################################################################
    # SMART health
    ###############################################################################
    smart = Smart(config.HDD_PATHS, log)
    smart_globalStatus = smart.getGlobalStatus()
    print(f"\n # Santé des disques : {'OK' if smart_globalStatus else 'KO'}")
    if not smart_globalStatus or args.details:
        print(smart.getGlobalDetails())


    ###############################################################################
    # Fail2ban service status
    ###############################################################################
    fail2ban = Fail2ban(log)
    fail2ban_globalStatus = fail2ban.getGlobalStatus()
    fail2ban_ip = fail2ban.getBannedIp()
    print(f"\n # Status de Fail2ban : {'OK' if fail2ban_globalStatus else 'KO'}")
    if not fail2ban_globalStatus or args.details:
        print(fail2ban.getGlobalDetails())
    if fail2ban_ip != "":
        print(f"Banned IP : {fail2ban_ip}")


    ###############################################################################
    # CPU status
    ###############################################################################
    """cpu = Cpu(log)
    cpu_globalStatus = cpu.getGlobalStatus()
    print(f"\n # Utilisation du CPU : {'OK' if cpu_globalStatus else 'KO'}")
    #cpu_globalStatus = False
    if not cpu_globalStatus:
        print(f"\t/!\\ Vérifier l'utilisation du CPU : {' '.join(cpu.checkCommand)}")"""

if __name__ == "__main__":
    main()
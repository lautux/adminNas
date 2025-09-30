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
from classes.df import Df
from classes.cpu import Cpu
from classes.mail import Mail


def main():
    result = ""
    parser = argparse.ArgumentParser(description="Script d'analyse du NAS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-d", "--details", action="store_true", help="Show more details")
    parser.add_argument("-m", "--mailto", type=str, default=config.MAIL_DEFAULT_RECIPIENT, help="Send result by mail to ...")
    args = parser.parse_args()
    loggingMode = config.LOGGING_MODE
    if(args.verbose):
        loggingMode = logging.DEBUG
        print(f"Activate verbose debug mode : {loggingMode}")

    log = Logger(f"{config.LOG_FILE_PATH}", loggingMode)
    if(args.verbose):
        print(f"Log file : {log.logFilePath}")
        if(args.mailto is not None):
            print(f"Send results to : {args.mailto}")
    


    ###############################################################################
    # Report header
    ###############################################################################
    result = f"{'-'*40}"
    result = f"{'Status du NAS': ^{40}}"
    result = f"{'-'*40}"


    ###############################################################################
    # RAID devices
    ###############################################################################
    raid = Raid(config.RAID_PATHS, log)
    raid_globalStatus = raid.getGlobalStatus()
    result = f"# Etat des RAID : {'OK' if raid_globalStatus else 'KO'}"
    if not raid_globalStatus or args.details:
        result = raid.getGlobalDetails()


    ###############################################################################
    # SMART health
    ###############################################################################
    smart = Smart(config.HDD_PATHS, log)
    smart_globalStatus = smart.getGlobalStatus()
    result = f"# Santé des disques : {'OK' if smart_globalStatus else 'KO'}"
    if not smart_globalStatus or args.details:
        result = smart.getGlobalDetails()


    ###############################################################################
    # Fail2ban service status
    ###############################################################################
    fail2ban = Fail2ban(log)
    fail2ban_globalStatus = fail2ban.getGlobalStatus()
    fail2ban_ip = fail2ban.getBannedIp()
    result = f"# Status de Fail2ban : {'OK' if fail2ban_globalStatus else 'KO'}"
    if not fail2ban_globalStatus or args.details:
        result = fail2ban.getGlobalDetails()
    if fail2ban_ip != "":
        result = f"Banned IP : {fail2ban_ip}"


    ###############################################################################
    # DF status
    ###############################################################################
    df = Df(config.DF_PATHS, log)
    df_globalStatus = df.getGlobalStatus()
    result = f"# Occupation des disques : {'OK' if df_globalStatus else 'KO'}"
    if not df_globalStatus or args.details:
        #result = df.getGlobalDetails(not args.details)
        result = df.getGlobalDetails()


    ###############################################################################
    # CPU status
    ###############################################################################
    """cpu = Cpu(log)
    cpu_globalStatus = cpu.getGlobalStatus()
    print(f"\n # Utilisation du CPU : {'OK' if cpu_globalStatus else 'KO'}")
    #cpu_globalStatus = False
    if not cpu_globalStatus:
        print(f"\t/!\\ Vérifier l'utilisation du CPU : {' '.join(cpu.checkCommand)}")"""
    
    print(result)
    if(args.mailto is not None):
        to_addr = args.mailto
        subject = "NAS - Health report"
        body = result
        mail = Mail(log)
        mail.send(to_addr, subject, body)


if __name__ == "__main__":
    main()
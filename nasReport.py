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
from classes.history import History


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
    result += f"{'-'*40}\n"
    result += f"{'Status du NAS': ^{40}}\n"
    result += f"{'-'*40}\n"


    ###############################################################################
    # RAID devices
    ###############################################################################
    raid = Raid(config.RAID_PATHS, log)
    raid_globalStatus = raid.getGlobalStatus()
    result += f"# Etat des RAID : {'OK' if raid_globalStatus else 'KO'}\n"
    if not raid_globalStatus or args.details:
        result += f"{raid.getGlobalDetails()}\n"


    ###############################################################################
    # SMART health
    ###############################################################################
    smart = Smart(config.HDD_PATHS, log)
    smart_globalStatus = smart.getGlobalStatus()
    result += f"# Santé des disques : {'OK' if smart_globalStatus else 'KO'}\n"
    if not smart_globalStatus or args.details:
        result += f"{smart.getGlobalDetails()}\n"


    ###############################################################################
    # Fail2ban service status
    ###############################################################################
    fail2ban = Fail2ban(log)
    fail2ban_globalStatus = fail2ban.getGlobalStatus()
    fail2ban_ip = fail2ban.getBannedIp()
    result += f"# Status de Fail2ban : {'OK' if fail2ban_globalStatus else 'KO'}\n"
    if not fail2ban_globalStatus or args.details:
        result += f"{fail2ban.getGlobalDetails()}\n"
    if fail2ban_ip != "":
        result += f"Banned IP : {fail2ban_ip}\n"


    ###############################################################################
    # DF status
    ###############################################################################
    df = Df(config.DF_PATHS, log)
    df_globalStatus = df.getGlobalStatus()
    result += f"# Occupation des disques : {'OK' if df_globalStatus else 'KO'}\n"
    if not df_globalStatus or args.details:
        #result = f"{df.getGlobalDetails(not args.details)}\n"
        result += f"{df.getGlobalDetails()}\n"


    ###############################################################################
    # DF history
    ###############################################################################
    dfHistory = History(log)
    dfHistory.getDfGraph(config.DF_HISTORY_PATH, config.DF_HISTORY_OUTPUT)
    
    print(result)
    if(args.mailto is not None):
        to_addr = args.mailto
        subject = "NAS - Health report"
        mail = Mail(log)
        bodyHTML = "<html><head><title>NAS Report</title></head>"
        bodyHTML+= "<body>"
        bodyHTML+= f"<pre>{result}</pre>"
        bodyHTML+= "<img src=\"cid:df_history\" alt=\"DF history\" />"
        bodyHTML+= "</body>"
        images = {
            "df_history": config.DF_HISTORY_OUTPUT,
        }
        mail.send(to_addr, subject, bodyHTML, images)


if __name__ == "__main__":
    main()
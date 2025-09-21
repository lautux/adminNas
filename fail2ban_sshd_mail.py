#!/usr/bin/env python3

"""
Script automatically called when an IP as been banned by fail2ban
Params :
        IP
        JAIL
        FAILLUES
        MATCHES
        IPMATCHES
"""

import logging
import config
import sys
from classes.logger import Logger
from classes.mail import Mail

# Getting command line parameters
fail2ban_ip = sys.argv[1]
fail2ban_jail = sys.argv[2]
fail2ban_failues = sys.argv[3]
fail2ban_matches = sys.argv[4]
fail2ban_ipmatches = sys.argv[5]

# Contenu de l'email
to_addr = "lautux76@gmail.com"
subject = "NAS - Fail2ban"
body = f"Tentative de connexion au NAS !\n\n\tDate : {fail2ban_matches}\n\tIP : {fail2ban_ip}\n\tNb de tentatives : {fail2ban_failues}"

log = Logger(f"{config.LOG_FILE_PATH}", logging.DEBUG)
mail = Mail(log)
print("mail.send() - DEBUT")
mail.send(to_addr, subject, body)
print("mail.send() - FIN")

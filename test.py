#!/usr/bin/env python3

import logging
import config
import sys
import subprocess
from classes.logger import Logger
from classes.mail import Mail

log = Logger(f"{config.LOG_FILE_PATH}", config.LOGGING_MODE)

resultat = subprocess.run(["python3", "nasReport.py", "-d"], capture_output=True, text=True)
print(f"{resultat.stdout}{("error :"+resultat.stderr) if not resultat.stderr else ""}")

"""mail = Mail(log)
print("mail.send() - DEBUT")
mail.send("lautux76@gmail.com", "test1", "bla bla bla")
print("mail.send() - FIN")"""



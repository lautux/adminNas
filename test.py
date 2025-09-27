#!/usr/bin/env python3

import logging
import config
import sys
import subprocess
from classes.logger import Logger
from classes.mail import Mail

log = Logger(f"{config.LOG_FILE_PATH}", config.LOGGING_MODE)

def exec(tabCmd):
    print(tabCmd)
    resultat = subprocess.run(tabCmd, capture_output=True, text=True)
    print(resultat.stdout)
    if not resultat.stderr:
        print(f"error :\n*{resultat.stderr}*")

exec(["python3", "nasReport.py"])
log.debug(f"{'#'*20} DEBUG {'#'*20}")
log.info(f"{'#'*20} INFO {'#'*20}")
log.warning(f"{'#'*20} WARNING {'#'*20}")
log.error(f"{'#'*20} ERROR {'#'*20}")
log.critical(f"{'#'*20} CRITICAL {'#'*20}")
exec(["python3", "nasReport.py", "-v"])
#exec(["python3", "nasReport.py", "-d", "-v"])


"""mail = Mail(log)
print("mail.send() - DEBUT")
mail.send("lautux76@gmail.com", "test1", "bla bla bla")
print("mail.send() - FIN")"""
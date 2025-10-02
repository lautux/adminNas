#!/usr/bin/env python3

import logging
import config
import sys
import subprocess
from classes.logger import Logger
from classes.mail import Mail
from classes.history import History

log = Logger(f"{config.LOG_FILE_PATH}", config.LOGGING_MODE)

def exec(tabCmd):
    print(tabCmd)
    resultat = subprocess.run(tabCmd, capture_output=True, text=True)
    print(resultat.stdout)
    if resultat.stderr:
        print(f"error :\n*{resultat.stderr}*")

#exec(["python3", "nasReport.py"])
#exec(["python3", "nasReport.py", "-d"])
#exec(["python3", "nasReport.py", "-m", "lautux76@gmail.com"])
#exec(["python3", "nasReport.py", "-d", "-v"])

dfHistory = History(log)
dfHistory.getDfGraph(config.DF_HISTORY_PATH, config.DF_HISTORY_OUTPUT)
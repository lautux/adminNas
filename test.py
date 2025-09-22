#!/usr/bin/env python3

import logging
import config
from classes.logger import Logger
from classes.mail import Mail

log = Logger(f"{config.LOG_FILE_PATH}", config.LOGGING_MODE)
mail = Mail(log)
print("mail.send() - DEBUT")
mail.send("lautux76@gmail.com", "test1", "bla bla bla")
print("mail.send() - FIN")



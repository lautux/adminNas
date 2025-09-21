#!/usr/bin/env python3

import logging
import config
from classes.logger import Logger
from classes.rclone import Rclone

log = Logger(f"{config.LOG_FILE_PATH}", logging.DEBUG)
rclone = Rclone(log)
print("rsync.sendData() - DEBUT")
rclone.sendData()
print("rsync.sendData() - FIN")
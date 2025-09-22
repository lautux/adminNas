#!/usr/bin/env python3

import logging
import config
from classes.logger import Logger
from classes.rclone import Rclone

log = Logger(f"{config.LOG_FILE_PATH}", config.LOGGING_MODE)
rclone = Rclone(log)
print("rsync.sendPhotos() - DEBUT")
rclone.sendPhotos()
print("rsync.sendPhotos() - FIN")
#! /usr/bin/python3

import smtplib
import config
import traceback
import os
import re
from classes.logger import Logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate

class Mail:
    """
    Class to send mail
    """
    logger = None

    def __init__(self, logger:Logger=None):
        """
        Constructor

        Parameters:
        logger (Logger): Logger object 
        """
        self.logger = logger


    def send(self, mailTo:str, mailSubject:str, mailBody:str, images:dict[str:str]=None) -> bool:

        # Avec le SMTP free.fr, on est obligé de mettre le même from que le compte utilisé pour s'authentifier sur le SMTP
        mailFrom = "merlet.l@free.fr"
        status = False
        
        # Envoi de l'email
        try:
            # Création du message
            msg = MIMEMultipart()
            msg['From'] = mailFrom
            msg['To'] = mailTo
            msg['Subject'] = mailSubject
            msg['Date'] = formatdate(localtime=True)
            if images:
                htmlCIDs = re.findall(r'src="cid:([^"]+)"', mailBody)
                for cid, path in images.items():
                    if cid in htmlCIDs:
                        if os.path.exists(path):
                            with open(path, 'rb') as fp:
                                img = MIMEImage(fp.read())
                                img.add_header('Content-ID', f'<{cid}>')
                                msg.attach(img)
            msg.attach(MIMEText(mailBody, 'html'))
            server = smtplib.SMTP(config.MAIL_SMTP, config.MAIL_PORT)
            server.starttls()  # Activer le mode TLS
            server.login(config.MAIL_USER, config.MAIL_PASSWORD)
            server.sendmail(mailFrom, mailTo, msg.as_string())
            server.quit()
            status = True
        except Exception as e:
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
              return status
#! /usr/bin/python3

import smtplib
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

class Mail:
    """
    Class to send mail
    """
    logger       = None

    def __init__(self, logger=None):
        """
        Constructor

        Parameters:
        logger (Logger): Logger object 
        """
        self.logger = logger


    def send(self, mailTo:str, mailSubject:str, mailBody:str) -> bool:

        # Avec le SMTP free.fr, on est obligé de mettre le même from que le compte utilisé pour s'authentifier sur le SMTP
        mailFrom = "merlet.l@free.fr"
        status = False
        
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = mailFrom
        msg['To'] = mailTo
        msg['Subject'] = mailSubject
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(mailBody, 'plain'))

        # Envoi de l'email
        try:
            server = smtplib.SMTP(config.MAIL_SMTP, config.MAIL_PORT)
            server.starttls()  # Activer le mode TLS
            server.login(config.MAIL_USER, config.MAIL_PASSWORD)
            server.sendmail(mailFrom, mailTo, msg.as_string())
            server.quit()
            status = True
        except Exception as e:
            self.logger.error(f"Error in Mail.send : {e.stderr}")
        finally:
              return status
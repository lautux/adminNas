#!/usr/bin/env python3

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

# recuperer les parametres de la ligne de commande
fail2ban_ip = sys.argv[1]
fail2ban_jail = sys.argv[2]
fail2ban_failues = sys.argv[3]
fail2ban_matches = sys.argv[4]
fail2ban_ipmatches = sys.argv[5]

# Configuration
smtp_server = "smtp.free.fr"
smtp_port = 587  # Port pour TLS
smtp_user = "merlet.l@free.fr"
smtp_password = "u6V!5XVxTjYFjx"

# Contenu de l'email
from_addr = "merlet.l@free.fr"
to_addr = "lautux76@gmail.com"
subject = "Test envoi mail"
body = f"Contenu du message :\n{fail2ban_ip} \n{fail2ban_jail} \n{fail2ban_failues} \n{fail2ban_matches} \n{fail2ban_ipmatches}"

# Création du message
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject
msg['Date'] = formatdate(localtime=True)
msg.attach(MIMEText(body, 'plain'))

# Envoi de l'email
try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Activer le mode TLS
        server.login(smtp_user, smtp_password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print("Email envoyé avec succès !")
except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")


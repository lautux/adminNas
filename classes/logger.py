#! /usr/bin/python3

import logging
from datetime import datetime

class Logger:
    def __init__(self, nom_fichier="app.log", niveau=logging.INFO):
        """
        Initialise le logger.

        Args:
            nom_fichier (str): Nom du fichier de log. Par défaut : "app.log".
            niveau (int): Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                         Par défaut : logging.INFO.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(niveau)
        self.logFilePath = nom_fichier

        # Formatteur pour les messages de log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Handler pour écrire dans un fichier
        file_handler = logging.FileHandler(nom_fichier)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Handler pour afficher dans la console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Écrit un message de niveau DEBUG."""
        self.logger.debug(message)

    def info(self, message):
        """Écrit un message de niveau INFO."""
        self.logger.info(message)

    def warning(self, message):
        """Écrit un message de niveau WARNING."""
        self.logger.warning(message)

    def error(self, message):
        """Écrit un message de niveau ERROR."""
        self.logger.error(message)

    def critical(self, message):
        """Écrit un message de niveau CRITICAL."""
        self.logger.critical(message)

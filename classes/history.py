#! /usr/bin/python3

import subprocess
import traceback
import config

class History:
    """
    Class to manage history data
    """
    logger       = None

    def __init__(self, logger=None):
        """
        Constructor

        Parameters:
        mountPoints (array): Linux mount points. Ex: /mnt/raid4to.
        """
        self.logger = logger

    def getDfGraph(self) -> bool:
        try:
            self.logger.debug(f"Df.getGlobalStatus - DEBUT")
            status = True
            for mnt in self.mountPoints:
                if not self.getDfStatus(mnt):
                    status = False
                    break
        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getGlobalStatus - FIN")
            return status

"""import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Charger le fichier (remplacez 'votre_fichier.txt')
with open("votre_fichier.txt", "r") as f:
    lines = f.readlines()

# Extraire les données
data = []
for line in lines:
    parts = line.split()
    if len(parts) >= 5:  # Vérifie que la ligne est valide
        timestamp = parts[0]
        used_perc = parts[4].replace('%', '')  # "1%" → "1"
        used_kb = parts[2]  # "288690" Ko
        mount_point = parts[-1]  # "/data"

        # Convertir la date (format: AAAAMMJJ_HHMMSS)
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")

        data.append({
            "datetime": dt,
            "used_perc": float(used_perc),
            "used_kb": int(used_kb),
            "mount_point": mount_point
        })

# Créer un DataFrame Pandas
df = pd.DataFrame(data)

# Filtrer pour un point de montage spécifique (ex: "/data")
df = df[df["mount_point"] == "/data"]
"""
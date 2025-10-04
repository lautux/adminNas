#! /usr/bin/python3

import traceback
from classes.logger import Logger
import config
from pathlib import Path
# Active virtual environment and install pandas + matplotlib :
# .\.venv\Scripts\Activate
# pip --proxy http://proxy.lynred.net:3128 install pandas
# pip --proxy http://proxy.lynred.net:3128 install matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class History:
    """
    Class to manage history data
    """
    logger       = None

    def __init__(self, logger:Logger=None):
        """
        Constructor

        Parameters:
        logger (Logger): A logger
        """
        self.logger = logger

    def getDfGraph(self, dataPath:str, outputFilePath:str) -> bool:
        try:
            self.logger.debug(f"Df.getDfGraph - DEBUT")
            status = True

            # 1. Get data from file
            dataDir = Path(dataPath)
            dataFiles = list(dataDir.glob(config.DF_HISTORY_FILE_FORMAT))
            df = pd.concat([pd.read_csv(f, sep=r'\s+', header=None, names=['timestamp', 'total', 'used', 'free', 'percent', 'partition']) for f in dataFiles], ignore_index=True)
            #df = pd.read_csv("C:/LAME/Perso/history/df_data2.txt", sep=r'\s+', header=None, names=['timestamp', 'total', 'used', 'free', 'percent', 'partition'])
            df['datetime'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
            df['percent'] = df['percent'].str.rstrip('%').astype(float)
            
            # 2. Build chart
            plt.figure(figsize=(12, 6))

            # 2.1. Select data
            partitions = df['partition'].unique()
            #partitions = [p for p in partitions if p not in ['/boot/efi', ]] # Exclude some partitions
            for partition in partitions:
                subset = df[df['partition'] == partition]
                plt.plot(subset['datetime'], subset['percent'], label=f"{partition}", marker='')
            plt.axhline(y=config.DF_THREATHOLD, color='orange', linestyle='--', label='Seuil critique')
            plt.ylim(0, 100)

            # 2.2. Customize chart
            plt.title("Évolution du volume occupé par les partitions")
            plt.xlabel("Date")
            plt.ylabel("Espace utilisé (%)")
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            
            # 3. Save picture
            plt.savefig(
                outputFilePath,
                dpi=300,
                bbox_inches='tight',
                transparent=False
            )

            # 4. Show chart
            #plt.show()

        except Exception as e:
            status = False
            self.logger.error(f"Exception occured : {traceback.format_exc()}")
        finally:
            self.logger.debug(f"Df.getDfGraph - FIN")
            return status


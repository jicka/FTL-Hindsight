import os
import shutil
import multiprocessing as mp
from datetime import datetime
from source import savegame as sg
from source import database_connector as db_con
from configparser import ConfigParser
from source import run as r
import copy
import numpy as np
from pprint import pprint
import time


# compile with pyinstaller.exe --onefile --windowed  ftl_savegame_manager.py


def initialize_saveparsing(parsing_active_event,shutdown_parsing_event):
    config = ConfigParser()
    config.read("config.ini")
    target_path = config["DEFAULT"]["target_path"]
    saves_db_path = config["DEFAULT"]["saves_db_path"]
    saves_new_path = config["DEFAULT"]["saves_new_path"]

    #Todo Remove cleanly
    target_path_mv = ""

    # ToDo: move this to settings.
    update_frequency = config["DEFAULT"]["update_frequency"]


    if not os.path.exists(saves_db_path):
        os.makedirs(saves_db_path)
    if not os.path.exists(saves_new_path):
        os.makedirs(saves_new_path)

    if update_frequency is None:
        update_frequency = 2

    tracking = False

    filename_suffix = ".sav"
    savegame = sg.Savegame(target_path, target_path_mv)

    # initialize
    runs = []
    beacons = 999
    last_run = None
    ship_name = None
    selected_run_index = 999

    print("DEBUG: Save file tracking process initialized.")
    print(parsing_active_event.wait(timeout=0))

    early_shutdown_trigger = False

    while not(shutdown_parsing_event.wait(timeout=0)) and not(early_shutdown_trigger):
        if parsing_active_event.wait(timeout=0):
            #track_file()
            print("DEBUG: track_file triggered")

        # Checking for shutdown before sleeping
        if shutdown_parsing_event.wait(timeout=0) == True:
            early_shutdown_trigger = True
            break

        #print("DEBUG: Sleeping")
        time.sleep(7)

    print("DEBUG: Save tracker closed.")



def track_file():
    if tracking:
        if os.path.exists(target_path) and not savegame.mv or os.path.exists(target_path_mv) and savegame.mv:
            try:
                savegame.parse()
                date_time_obj = datetime.now()
                timestamp_str = date_time_obj.strftime("%Y-%b-%d %H-%M-%S")
                # check if new ship is played
                if savegame.run.total_beacons_explored < beacons or savegame.run.ship_name != ship_name:
                    foldername = "%s-%s" % (timestamp_str, savegame.run.ship_name)
                    folder_path = os.path.join(saves_new_path, foldername)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        update_statusbar("folder created")
                    if beacons != 999: # don't append if it's the first run since starting the program
                        runs.append(last_run)
                    beacons = 0
                ship_name = savegame.run.ship_name
                last_run = copy.deepcopy(savegame.run)

                if savegame.run.total_beacons_explored > beacons:
                    beacons = savegame.run.total_beacons_explored
                    filename = "%s(%s)-%s-%s" % (
                    str(beacons), savegame.run.sector, savegame.run.ship_name, timestamp_str)
                    new_path = os.path.join(folder_path, filename + filename_suffix)
                    latest_filepath = new_path
                    if savegame.mv:
                        shutil.copy(target_path_mv, new_path)
                    else:
                        shutil.copy(target_path, new_path)
                    update_statusbar(filename + " copied")
                    update_run_detail()
                    update_run_overview()
            except Exception:
                print("file is currently in use")
            print("saving to db...")

            # SQL CODE

            print("saving done.")
        print("running...")
    






if __name__ == '__main__':
    print ("ERROR: This code should be started from hindsight.py")




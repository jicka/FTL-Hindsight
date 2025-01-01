from configparser import ConfigParser


def create_initial_config ():
    # Read config file
    config = ConfigParser()
    #config.read("config.ini")

    # target_path: this has to be the location where FTL stores the continue.sav.
    config["PATHS"] = {"target_path": "~/.local/share/FasterThanLight/continue.sav",
                     "save_files_backup_path": "~/Applications/FTL/FTL-Hindsight/data/saves",
                     "db_path": "~/Applications/FTL/FTL-Hindsight/data/"}

    config["SETTINGS"] = {"auto_tracking": "True",
                     "update_frequency": "2000",
                     "default_tab": "1",
                     "default_spoiler_level": "0"}

    with open('config.ini', 'w') as configfile:
      config.write(configfile)

if __name__ == '__main__':
    create_initial_config()


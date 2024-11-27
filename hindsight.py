import tkinter as tk
from tkinter import ttk
import os
import shutil
from datetime import datetime
from source import savegame as sg
from source import database_connector as db_con
from configparser import ConfigParser
from source import run as r
import copy
import numpy as np
from pprint import pprint



#customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
#customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



global app_title
global lbl_manage_profiles
global lbl_profile
global spoiler_level
global default_score_filter

app_title = "FTL - Hindsight"
default_spoiler_level = 0
spoiler_level = 0
default_score_filter = 5000

# --- LABELS ---
lbl_placeholder = "This is a placeholder"
lbl_manage_profiles = "Manage Profiles"
lbl_profile = "Profile:"
lbl_spoiler = "Spoiler Level:"
lbl_spoiler_0 = "No Spoilers"
lbl_spoiler_1 = "General Info"
lbl_spoiler_2 = "All Details"
lbl_settings_button = "Settings"
lbl_about_button = "About"
lbl_tab_statistics = "Global Statistics"
lbl_tab_run_review = "Single Run Review"
lbl_tab_current_save = "Current Save Insights"
lbl_filter_empty = "-"
lbl_filter_shiptype = "Ship Type"
lbl_filter_shipvar = "Variant"
lbl_filter_victory = "Run Victory"
lbl_filter_victory_val = "Victory"
lbl_filter_defeat_val = "Defeat"
lbl_filter_score = "Score"
lbl_filter_above = "Above"
lbl_filter_below = "Below"
lbl_filter_submit = "Submit"




# ---- TopBarFrame ----

class TopBarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.style = ttk.Style()
        self.style.configure("spoiler_slider.Horizontal.TScale", background="#31363b")

        self.spoiler_level_var = tk.IntVar()
        self.spoiler_level_var.set(spoiler_level)
        self.topbar_spoiler_value_label = tk.StringVar()
        self.topbar_spoiler_value_label.set(lbl_spoiler_0)

        self.columnconfigure((0,1,2,3), weight=1)

        self.topbar_logo_label = ttk.Label(self, text=app_title)
        self.topbar_logo_label.grid(row=0, column=0, padx=0, pady=0)
        self.topbar_logo_label.rowconfigure(0, weight=1)

        
        # Frame to group profile label, drop-down and button
        self.topbar_profile_frame = ttk.Frame(self)
        self.topbar_profile_frame.grid(row=0, column=1, sticky="nsew")
        self.topbar_profile_frame.rowconfigure(0, weight=1)

        self.topbar_profile_label = ttk.Label(self.topbar_profile_frame, text=lbl_profile, anchor="e")
        self.topbar_profile_label.grid(row=0, column=0, padx=(5,2), pady=2)
        self.topbar_profile_optionsmenu = ttk.Combobox(self.topbar_profile_frame, values=["Pause", "NoPause", "Easy"])
        self.topbar_profile_optionsmenu.grid(row=0, column=1, padx=(0,5), pady=2)

        self.topbar_profile_button = ttk.Button(self.topbar_profile_frame, command=self.topbar_manage_profiles_event, text=lbl_manage_profiles)
        self.topbar_profile_button.grid(row=0, column=2, padx=0, pady=2)


        # Spoiler level
        self.topbar_spoiler_frame = ttk.Frame(self)
        self.topbar_spoiler_frame.grid(row=0, column=2, sticky="nsew")
        self.topbar_spoiler_frame.rowconfigure(0, weight=1)

        self.topbar_spoiler_label = ttk.Label(self.topbar_spoiler_frame, text=lbl_spoiler, anchor="e")
        self.topbar_spoiler_label.grid(row=0, column=0, padx=(5,2), pady=0)
        
        self.topbar_spoiler_level = ttk.Scale(self.topbar_spoiler_frame, orient=tk.HORIZONTAL, variable=self.spoiler_level_var, style="spoiler_slider.Horizontal.TScale", command=self.topbar_spoiler_event, from_=0, to=2, length=150)
        self.topbar_spoiler_level.set(default_spoiler_level)
        self.topbar_spoiler_level.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

        self.topbar_spoiler_value = ttk.Label(self.topbar_spoiler_frame, textvariable=self.topbar_spoiler_value_label, anchor="w")
        self.topbar_spoiler_value.grid(row=0, column=2, padx=(0,5), pady=(0, 0))


        # Settings Button
        self.topbar_settings_button = ttk.Button(self, command=self.topbar_manage_profiles_event, text=lbl_settings_button)
        self.topbar_settings_button.grid(row=0, column=3, padx=0, pady=2)

        # About Button
        self.topbar_settings_button = ttk.Button(self, command=self.topbar_manage_profiles_event, text=lbl_about_button)
        self.topbar_settings_button.grid(row=0, column=4, padx=(0,5), pady=2)



    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        return checked_checkboxes

    def topbar_manage_profiles_event(self):
        print("topbar_manage_profiles_event click")

    def change_profile_event(self, profile: str):
        print("topbar_manage_profiles_event selected: " + profile)

    def topbar_spoiler_event(self, level_str):
        self.level = int(float(level_str))
        print(level_str)
        print(":")
        print(self.level)
        spoiler_level = self.level
        self.spoiler_level_var.set(self.level)

        if self.level == 2:
            self.topbar_spoiler_value_label.set(lbl_spoiler_2)
            self.style.configure("spoiler_slider.Horizontal.TScale", background="red")
        elif self.level == 1:
            self.topbar_spoiler_value_label.set(lbl_spoiler_1)
            self.style.configure("spoiler_slider.Horizontal.TScale", background="gold")
        else:
            self.topbar_spoiler_value_label.set(lbl_spoiler_0)
            self.style.configure("spoiler_slider.Horizontal.TScale", background="#31363b")





# ---- GlobalStatisticsTabFrame ----

class GlobalStatisticsTabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0,1,2,3), weight=1)
        self.rowconfigure((0,1,2,3), weight=1)

        self.placeholder = ttk.Label(parent, text=lbl_placeholder)
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)





# ---- TAB ----
# ---- SingleRunReviewTabFrame ----

# ---- SUB-FRAMES ----

# ---- Run Selector (Filters and List frames) Frame
class SingleRunReviewTabFrameRunSelectorFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


        self.score_filter = tk.StringVar()
        self.score_filter.set(default_score_filter)


        self.columnconfigure((0,1,2,3), weight=1)
        self.rowconfigure((0,1,2), weight=0)
        self.rowconfigure((3), weight=1)


        self.filter_shiptype_label = ttk.Label(self, text=lbl_filter_shiptype, anchor="e")
        self.filter_shiptype_label.grid(row=0, column=0, padx=(5,2), pady=2)
        #Todo: replace ship types by a dynamic system based on a dictionnary of available ship types.
        self.filter_shiptype = ttk.Combobox(self, values=[lbl_filter_empty, "Federation", "Mantis", "Lanius"])
        self.filter_shiptype.grid(row=0, column=1, padx=(0,5), pady=2)

        self.filter_shipvar_label = ttk.Label(self, text=lbl_filter_shipvar, anchor="e")
        self.filter_shipvar_label.grid(row=0, column=2, padx=(5,2), pady=2)
        #Todo: replace A, B, C by a dynamic system based on a dictionnary of available ship types.
        self.filter_shipvar = ttk.Combobox(self, values=[lbl_filter_empty, "A", "B", "C"])
        self.filter_shipvar.grid(row=0, column=3, padx=(0,5), pady=2)

        self.filter_victory_label = ttk.Label(self, text=lbl_filter_victory, anchor="e")
        self.filter_victory_label.grid(row=1, column=0, padx=(5,2), pady=2)
        self.filter_victory = ttk.Combobox(self, values=[lbl_filter_empty, lbl_filter_victory_val, lbl_filter_defeat_val])
        self.filter_victory.grid(row=1, column=1, padx=(0,5), pady=2)


        self.filter_score_label = ttk.Label(self, text=lbl_filter_score, anchor="e")
        self.filter_score_label.grid(row=2, column=0, padx=(5,2), pady=2)
        self.filter_type_score = ttk.Combobox(self, values=[lbl_filter_empty,lbl_filter_above,lbl_filter_below])
        self.filter_type_score.grid(row=2, column=1, padx=(0,5), pady=2)
        self.filter_score = ttk.Scale(self, from_=0, to=10000, length=150, orient=tk.HORIZONTAL, command=self.filter_score_change)
        self.filter_score.set(default_score_filter)
        self.filter_score.grid(row=2, column=2, padx=0, pady=0, sticky="ew")
        self.filter_score_value_label = ttk.Label(self, textvariable=self.score_filter, anchor="w")
        self.filter_score_value_label.grid(row=2, column=3, padx=(0,5), pady=(0, 0))

        # self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameRunSelectorFrame")
        # self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)
        # self.placeholder.rowconfigure(0, weight=1)

        # Create the systems list frame
        self.run_selector_list_frame = SingleRunReviewTabFrameRunSelectorListFrame(self)
        self.run_selector_list_frame.grid(row=3, column=0, sticky="nsew", columnspan=4)
        self.run_selector_list_frame.rowconfigure(0, weight=1)

    def change_filter_event(self, filter_value: str):
        print("filter changed: " + filter_value)

    def filter_score_change(self, val: str):
        self.score_filter.set(int(float(val)))




# ---- Run Selector List (List frame) Frame
class SingleRunReviewTabFrameRunSelectorListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)

        self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameRunSelectorListFrame")
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)

# ---- Run Selector List (List frame) Frame
class SingleRunReviewTabFrameRunSelectorListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)

        self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameRunSelectorListFrame")
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)


# ---- Run Sector Overview Frame
class SingleRunReviewTabFrameSectorListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)

        self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameSectorListFrame")
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0, sticky="nsew")


# ---- Run Sector Overview Frame
class SingleRunReviewTabFrameJumpListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)

        self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameJumpListFrame")
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)



# ---- Run Sector Overview Frame
class SingleRunReviewTabFrameOwnShipFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)

        self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameOwnShipFrame")
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)




# ---- Run Sector Overview Frame
class SingleRunReviewTabFrameEnemyShipFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=1)

        self.placeholder = ttk.Label(self, text="SingleRunReviewTabFrameEnemyShipFrame")
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)



# ---- MAIN-FRAME ----

class SingleRunReviewTabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        parent.columnconfigure((0,1,2,3), weight=1)
        parent.rowconfigure((0,1), weight=1)

        self.columnconfigure((0,1,2,3), weight=1)
        self.rowconfigure((0,1), weight=1)

        # Frame to filter runs and select one from a list
        self.runfilter_frame = SingleRunReviewTabFrameRunSelectorFrame(parent)
        #self.runfilter_frame = ttk.Label(parent, text="Run Filter")
        self.runfilter_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        
         # Frame to see sector list (with short summary) and select one
        self.sectorlist_frame = SingleRunReviewTabFrameSectorListFrame(parent)
        #self.sectorlist_frame = ttk.Label(parent, text="Sector List")
        self.sectorlist_frame.grid(row=0, column=1, columnspan=3, sticky="nsew")

         # Frame to see jump list (with short summary) and select one
        self.jumplist_frame = SingleRunReviewTabFrameJumpListFrame(parent)
        #self.jumplist_frame = ttk.Label(parent, text="Jump List")
        self.jumplist_frame.grid(row=1, column=1, sticky="nsew")

         # Frame to see jump list (with short summary) and select one
        self.ownship_frame = SingleRunReviewTabFrameOwnShipFrame(parent)
        #self.ownship_frame = ttk.Label(parent, text="Own Ship Info")
        self.ownship_frame.grid(row=1, column=2, sticky="nsew")

         # Frame to see jump list (with short summary) and select one
        self.enemyship_frame = SingleRunReviewTabFrameEnemyShipFrame(parent)
        #self.enemyship_frame = ttk.Label(parent, text="Enemy Ship Info")
        self.enemyship_frame.grid(row=1, column=3, sticky="nsew")



    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        return checked_checkboxes












# ---- CurrentSaveTabFrame ----

class CurrentSaveTabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((1,2,3,4), weight=1)
        self.placeholder = ttk.Label(parent, text=lbl_placeholder)
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)

        




























class App(tk.Tk):
    def __init__(self):
        super().__init__()

        config = ConfigParser()
        config.read("config.ini")
        self.target_path = config["DEFAULT"]["target_path"]
        self.saves_db_path = config["DEFAULT"]["saves_db_path"]
        self.saves_new_path = config["DEFAULT"]["saves_new_path"]

        #Todo Remove cleanly
        self.target_path_mv = ""

        # ToDo: move this to settings.
        self.update_frequency = config["DEFAULT"]["update_frequency"]


        if not os.path.exists(self.saves_db_path):
            os.makedirs(self.saves_db_path)
        if not os.path.exists(self.saves_new_path):
            os.makedirs(self.saves_new_path)

        if self.update_frequency is None:
            self.update_frequency = 2000

        self.tracking = False

        self.filename_suffix = ".sav"
        self.savegame = sg.Savegame(self.target_path, self.target_path_mv)







        # Configure window
        self.title(app_title)
        self.geometry(f"{1280}x{720}")
        self.tk.call('source', '/home/jonas/Applications/FTL/tkBreeze/breeze-dark/breeze-dark.tcl')
        s = ttk.Style()
        s.theme_use('breeze-dark')

        # Configure grid layout (4x4)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)


        # Create the top menu bar
        self.topbar_frame = TopBarFrame(self)
        self.topbar_frame.grid(row=0, column=0, sticky="new")
        self.topbar_frame.rowconfigure(0, weight=0)

        self.tabview = ttk.Notebook(self)
        self.tabview.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.tabview.columnconfigure(0, weight=1)

        self.stats_tab_frame_frame = ttk.Frame()
        self.single_run_tab_frame_frame = ttk.Frame()
        self.current_save_tab_frame_frame = ttk.Frame()

        self.tabview.add(self.stats_tab_frame_frame, text=lbl_tab_statistics)
        self.tabview.add(self.single_run_tab_frame_frame, text=lbl_tab_run_review)
        self.tabview.add(self.current_save_tab_frame_frame, text=lbl_tab_current_save)

        # Fill the tabs with the respective frames
        self.stats_tab_frame = GlobalStatisticsTabFrame(self.stats_tab_frame_frame)
        self.single_run_tab_frame = SingleRunReviewTabFrame(self.single_run_tab_frame_frame)
        self.current_save_tab_frame = CurrentSaveTabFrame(self.current_save_tab_frame_frame)




        # --- EVENTS ---




if __name__ == "__main__":
    app = App()
    app.mainloop()

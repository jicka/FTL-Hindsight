import tkinter
import tkinter.messagebox
import customtkinter
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



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



global app_title
global lbl_manage_profiles
global lbl_profile
global spoiler_level

app_title = "FTL - Hindsight"
default_spoiler_level = 0
spoiler_level = 0

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



# ---- TopBarFrame ----

class TopBarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0,1,2,3), weight=1)


        self.topbar_logo_label = customtkinter.CTkLabel(self, text=app_title, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.topbar_logo_label.grid(row=0, column=0, padx=0, pady=0)
        
        # Frame to group profile label, drop-down and button
        self.topbar_profile_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.topbar_profile_frame.grid(row=0, column=1, sticky="ew")
        self.topbar_profile_frame.grid_rowconfigure(0, weight=1)

        self.topbar_profile_label = customtkinter.CTkLabel(self.topbar_profile_frame, text=lbl_profile, anchor="e")
        self.topbar_profile_label.grid(row=0, column=0, padx=(5,2), pady=2)
        self.topbar_profile_optionsmenu = customtkinter.CTkOptionMenu(self.topbar_profile_frame, values=["Pause", "NoPause", "Easy"], command=self.change_profile_event)
        self.topbar_profile_optionsmenu.grid(row=0, column=1, padx=(0,5), pady=2)

        self.topbar_profile_button = customtkinter.CTkButton(self.topbar_profile_frame, command=self.topbar_manage_profiles_event, text=lbl_manage_profiles)
        self.topbar_profile_button.grid(row=0, column=2, padx=0, pady=2)


        # Spoiler level
        self.topbar_spoiler_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.topbar_spoiler_frame.grid(row=0, column=2, sticky="nsew")
        self.topbar_spoiler_frame.grid_rowconfigure(0, weight=1)

        self.topbar_spoiler_label = customtkinter.CTkLabel(self.topbar_spoiler_frame, text=lbl_spoiler, anchor="e")
        self.topbar_spoiler_label.grid(row=0, column=0, padx=(5,2), pady=0)
        
        self.topbar_spoiler_level = customtkinter.CTkSlider(self.topbar_spoiler_frame, from_=0, to=2, number_of_steps=2, command=self.topbar_spoiler_event)
        self.topbar_spoiler_level.set(default_spoiler_level)
        self.topbar_spoiler_level.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

        self.topbar_spoiler_value = customtkinter.CTkLabel(self.topbar_spoiler_frame, text=lbl_spoiler_0, anchor="w")
        self.topbar_spoiler_value.grid(row=0, column=2, padx=(0,5), pady=(0, 0))


        # Settings Button
        self.topbar_settings_button = customtkinter.CTkButton(self, command=self.topbar_manage_profiles_event, text=lbl_settings_button)
        self.topbar_settings_button.grid(row=0, column=3, padx=0, pady=2)

        # About Button
        self.topbar_settings_button = customtkinter.CTkButton(self, command=self.topbar_manage_profiles_event, text=lbl_about_button)
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

    def topbar_spoiler_event(self, level: str):
        spoiler_level = level
        if level == 2:
            self.topbar_spoiler_value.configure(text=lbl_spoiler_2)
            self.topbar_spoiler_level.configure(progress_color=("red", "darkred"))
        elif level == 1:
            self.topbar_spoiler_value.configure(text=lbl_spoiler_1)
            self.topbar_spoiler_level.configure(progress_color=("yellow", "gold"))
        else:
            self.topbar_spoiler_value.configure(text=lbl_spoiler_0)
            self.topbar_spoiler_level.configure(progress_color=("gray40", "#AAB0B5"))





# ---- GlobalStatisticsTabFrame ----

class GlobalStatisticsTabFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)

        self.placeholder = customtkinter.CTkLabel(master, text=lbl_placeholder)
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)



    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        return checked_checkboxes







# ---- SingleRunReviewTabFrame ----

class SingleRunReviewTabFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((1,2,3,4), weight=1)
        self.placeholder = customtkinter.CTkLabel(master, text=lbl_placeholder)
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)

        



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

class CurrentSaveTabFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((1,2,3,4), weight=1)
        self.placeholder = customtkinter.CTkLabel(master, text=lbl_placeholder)
        self.placeholder.grid(row=0, column=0, padx=(20,20), pady=0)

        



    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        return checked_checkboxes
























class App(customtkinter.CTk):
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

        # Configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1), weight=1)


        # Create the top menu bar
        self.topbar_frame = TopBarFrame(self)
        self.topbar_frame.grid(row=0, column=0, sticky="new")
        self.topbar_frame.grid_rowconfigure(0, weight=0)




        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.tabview.grid_columnconfigure(0, weight=1)
        self.tabview.add(lbl_tab_statistics)
        self.tabview.add(lbl_tab_run_review)
        self.tabview.add(lbl_tab_current_save)

        self.tabview.tab(lbl_tab_statistics).grid_columnconfigure(0, weight=1)
        self.tabview.tab(lbl_tab_run_review).grid_columnconfigure(0, weight=1)
        self.tabview.tab(lbl_tab_current_save).grid_columnconfigure(0, weight=1)

        self.tabview.tab(lbl_tab_statistics).grid_rowconfigure(0, weight=1)
        self.tabview.tab(lbl_tab_run_review).grid_rowconfigure(0, weight=1)
        self.tabview.tab(lbl_tab_current_save).grid_rowconfigure(0, weight=1)

        # Fill the tabs with the respective frames
        self.stats_tab_frame = GlobalStatisticsTabFrame(self.tabview.tab(lbl_tab_statistics))
        self.single_run_tab_frame = SingleRunReviewTabFrame(self.tabview.tab(lbl_tab_run_review))
        self.current_save_tab_frame = CurrentSaveTabFrame(self.tabview.tab(lbl_tab_current_save))



        # --- EVENTS ---




if __name__ == "__main__":
    app = App()
    app.mainloop()

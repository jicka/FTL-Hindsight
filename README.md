# FTL Hindsight

## Note
I just started writing the tool, there is currently nothing functional. This page reflects what I want to tool to become.

FTL Hindsight is a heavily modified version of the FTL Savegame Manager designed to record all of your FTL gameplay to give you better insights into your game.

## Functionality
### Global Statistics
FTL-Hindsight tracks jump, sector and run data for all your runs. The tool allows you to get statistics on each level, allowing you to get specific knowledge out of your runs. For instance:
- What is my win-rate per ship?
- How much lower is my average first-sector scrap when I loose a run compared to successful runs?
- What is my average reactor level at the end of the run? 

### Single Run Review
Do a deep dive into specific runs, showing you sector and jump details as well as statistics. This is an extension on what the FTL Savegame Manager allowed to do:
- Per sector / jump changes in:
	- Scrap
	- Hull
	- Inventory
	- Crew
	- Systems
- Jump details showing event / store information when available.

# Background
A few months ago, after watching some advanced tutorials on FTL (special thank you to Crow for all the amazing videos), I decided to improve my level and started playing on hard after years playing normal difficulty. While micromanagement mistakes give immediate feedback, I struggle to perceive slight strategic mistakes where the consequences can only be felt many jumps later. For that I wanted to be able to review my decision-making after the run was over. My understanding is that the current best way of doing so is recording full videos of every run and then looking at the video. This is not something I was interested in,
so I decided to try to build a tool that helps with that, using the excellent FTL Savegame Manager as base.

And because I have to collect detailed run data anyway, I want to replace manually tracking global run stats in a table with this tool.

# Disclaimers

## Compatibility
I only tested this program for the Steam Version 1.6.13 running Linux. If you're using a diffrent version the program might crash trying to read the save-file. Mods that alter save files will not be compatible.

The code should work on other platforms.

## In-Game Error Messages
There is a very small chance that FTL will try to access the current save file at the same time as this program. If that happens there will be an message in FTL saying that it was unable to save. This is unproblematic, FTL will save your progress again on the next beacon.

## Code Quality
I am not a programmer and this is my first time writing Python. As such, code quality will certainly be very low (in ways I do not understand). Apologies in advance to anyone reading the code. If you have advice / improvement ideas, please let me know.

# Credits

A lot of the code structure is inherited from ejms116's [FTL Savegame Manager](https://github.com/ejms116/FTL_Savegame_Manager).

The code that reads the continue.sav file is based on [Vhati's profile editor](https://github.com/Vhati/ftl-profile-editor) and the [python implementation by whiskeythecat](https://github.com/whiskeythecat/ftl_twitch).

The idea for the tool stems from Crow Revell's excellent points on the tendency to focus on short-term RNG and micromanagement mistakes, instead of looking at the overall decision-making that made the ship weaker in the first place.

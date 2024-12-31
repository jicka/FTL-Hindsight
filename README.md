# FTL Hindsight

## Note
I just started writing the tool, there is currently nothing functional.

FTL Hindsight is a heavily modified version of the FTL Savegame Manager designed to record all of your FTL gameplay. The tool allows you to:
1. See detailed statistics on your runs, including the ability to apply filters.
2. Do a deep dive into specific runs, showing you sector and jump details.

# Background
A few months ago, after watching some advanced tutorials on FTL (special mention to Crow's videos), I decided to improve my level and I started playing on hard after years playing normal difficulty. While micromanagement mistakes give immediate feedback, I struggle to perceive slight strategic mistakes where the consequences can only be felt many jumps later. For that I wanted to be able to review runs after the fact. My understanding is that the current best way of doing so is recording full videos of every run. This is not something I was interested in.
So I decided to try to build a tool that helps with that, using the excellent FTL Savegame Manager as base.

# Disclaimers

## Compatibility
I only tested this program for the Steam Version 1.6.14 running Linux. If you're using a diffrent version the program might crash trying to read the save-file. Mods that alter save files will not be compatible.

The code should work on other platforms.

## In-Game Error Messages
Also note that there is a very small chance that FTL will try to access the current save file at the same time as this program. If that happens there will be an message in FTL saying that it was unable to save. This is unproblematic, FTL will save your progress again on the next beacon.

## Code Quality
I am not an experienced programmed and this is my first time writing Python. As such, code quality will certainly be very low (in ways I do not understand yet). Apologies in advance to anyone reading the code. If you have advice / improvement ideas, please let me know.

# Credits

A lot of the code structure is inherited from ejms116's [FTL Savegame Manager](https://github.com/ejms116/FTL_Savegame_Manager).

The code that reads the continue.sav file is based on [Vhati's profile editor](https://github.com/Vhati/ftl-profile-editor) and the [python implementation by whiskeythecat](https://github.com/whiskeythecat/ftl_twitch).



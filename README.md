RetroPy Portable Multi-Console Emulator v1.1.0-alpha

This is a portable Python multi-console emulator using PyBoy and Pygame.
It allows you to run Game Boy, Game Boy Advance, NES, SNES, N64, GameCube/Wii, and PSP games from a folder — no system-wide Python installation needed.

Folder Structure

Your folder should look like this:

RetroPy/
├── retropy.py               # Main launcher script
├── Python313/               # Portable Python folder
│    ├── python.exe
│    ├── pythonw.exe
│    ├── python313.dll
│    ├── python313.zip
│    ├── python313._pth
│    ├── Scripts/
│    └── Lib/
├── Roms/                    # Folder containing your ROMs
└── Assets/
     ├── background.png      # Optional background image
     └── icon.png            # Optional launcher icon

Downloading Portable Python

Go to the official Python release page:
https://www.python.org/downloads/windows/

Download the "Windows embeddable package (64-bit)" for Python 3.13.

Extract the ZIP file into the folder RetroPy/Python313.

The folder must contain python.exe directly inside it.

(Optional) Add pip if not included:

Download get-pip.py from https://bootstrap.pypa.io/get-pip.py
Run: D:\RetroPy\Python313\python.exe get-pip.py


Open python313._pth in a text editor and remove the # from #import site.

Run PowerShell to create necessary directories:

mkdir D:\Python313\Lib
mkdir D:\Python313\Lib\site-packages

Installing Required Packages

Open PowerShell in the RetroPy folder and run:

D:\RetroPy\Python313\python.exe -m pip install pyboy pygame


This installs PyBoy and Pygame for your portable Python.

Packages are installed inside the Python313 folder.

Running the Emulator

Ensure your folder structure is intact.

Run the emulator:

Option A: Double-click retropy.py
Option B: Run via command line:

D:\Python313\python.exe D:\RetroPy\retropy.py

ROMs

Place your ROM files inside Roms/:

.gb, .gbc → Game Boy / Game Boy Color

.gba → Game Boy Advance

.nes, .fds → NES / Famicom Disk System

.smc, .sfc → SNES

.n64, .z64 → N64

.iso, .gcm → GameCube/Wii

.iso, .cso → PSP

Optional: add cover.png and desc.txt for each ROM to show thumbnails and descriptions.

Subfolders inside Roms/ are supported.

Settings

Access Settings in the launcher to adjust:

Scroll Speed

Zoom (center & side)

Sound volume

ROM folder name

Emulator paths for:

Game Boy Advance (mGBA)

NES

SNES

N64

Dolphin (GameCube/Wii)

PPSSPP (PSP)

License

Include your preferred license here. For example:

MIT License

Copyright (c) 2025 Leo59063

Permission is hereby granted, free of charge, to any person obtaining a copy...

Enjoy your portable RetroPy v1.1.0-alpha multi-console emulator!

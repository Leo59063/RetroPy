RetroPy Portable Gameboy Emulator
=================================

This is a portable Python Gameboy emulator using PyBoy and Pygame.
It runs entirely from a folder without installing Python system-wide.
(This is meant for a drive)

Folder Structure
----------------
Your folder should look like this:
```text
RetroPy/
├── retropy.py           # Main launcher script
├── Python313/           # Portable Python folder
│    ├── python.exe
│    ├── pythonw.exe
│    ├── python313.dll
│    ├── python313.zip
|    ├── python313._pth
│    ├── Scripts/
│    └── Lib/
├── Roms/                # Folder containing your ROMs
└── Assets/
     └── background.png  # Optional background image

Downloading Portable Python
---------------------------
1. Go to the official Python release page:
   https://www.python.org/downloads/windows/
2. Download the **"Windows embeddable package (64-bit)"** for Python 3.13.
3. Extract the ZIP file into the folder `PYBOY/Python313`.
   - The folder must contain `python.exe` directly inside it.
4. (Optional) Add pip if not included:
   - Download `get-pip.py` from https://bootstrap.pypa.io/get-pip.py
   - Run: `D:\PYBOY\Python313\python.exe get-pip.py`
   - This will install pip in the portable Python.
5. Open python313._pth in a text editor and remove the # from "#import site"
6. Run "mkdir E:\Python313\Lib" In PowerShell
7. Run "mkdir E:\Python313\Lib\site-packages  

Installing Required Packages
----------------------------
Open PowerShell in the `RetroPy` folder and run:

D:\PYBOY\Python313\python.exe -m pip install pyboy pygame

- This installs PyBoy and Pygame for your portable Python.
- All packages will be installed **inside the Python313 folder**.

Running the Emulator
-------------------
1. Make sure your folder structure is intact.
2. Run the emulator:

Option A: Double-click `retropy.py`  
Option B: Run via command line:


D:\Python313\python.exe D:\RetroPy\retropy.py

ROMs
----
- Place your `.gb` and `.gbc` files inside `Roms/`.
- Optional: add `cover.png` and `desc.txt` for each ROM to show thumbnails and descriptions.
- The launcher also supports ROMs inside subfolders.

Settings
--------
- Access the `Settings` item in the launcher to adjust:
    - Scroll Speed
    - Zoom (center & side)
    - Sound volume
    - ROM folder name

License
-------
Include your preferred license here.
MIT License

Copyright (c) 2025 Leo59063

Permission is hereby granted, free of charge, to any person obtaining a copy

---

Enjoy your portable Gameboy emulator!

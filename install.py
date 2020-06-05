#!/bin/python2.7
import sys
import os


argv = sys.argv;
argc = len(argv);
dir = "/";
if(argc != 1):
	dir = argv[1];
os.system("mkdir -p " + dir + "/usr/bin/");
os.system("cp wine_hardened_script_gui.py " + dir+  "/usr/bin/wine-security-gui");
os.system("cp steam_security.py " + dir+  "/usr/bin/steam-security");
os.system("cp wine_no_internet.py " + dir+  "/usr/bin/wine-no-internet");
os.system("chmod +x -R "+  dir);


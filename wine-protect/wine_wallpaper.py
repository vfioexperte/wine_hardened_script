#!/usr/bin/env python
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
version = "0.2a"
print(version);

import sys
import os
import os.path
import platform
import string
import subprocess

reg_hak_file = "/usr/share/wine-security-gui/wallpaper_hak.reg"

appname = "wine_wallpaper";

debug_fodler = "";


#-scale 3840x2640
#from Sebs Downsample App imported

def cmd_start(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True).decode().split("\n")
        return out
    except subprocess.CalledProcessError:
        return []

def read_monitor_auflosung():
    s2 = cmd_start("xrandr --listmonitors ")
    monitore = -1
    j = 0
    hdmi = []
    auflosung = []
    for tmp in s2:
        s3 = tmp.split(" ")
        #print(s3)
        if(s3[0] == "Monitors:"):
            monitore = int(s3[1])
            continue
        if(len(s3) <= 5):
            continue
        else:
            if(j >= monitore):
                continue
            if(s3[1] == str(j) + ":"):
                hdmi.append(s3[5])
                s4 = s3[3].split("x")
                # print(s4);
                s5 = s4[0].split("/")
                x = s5[0]
                s5 = s4[1].split("/")
                y = s5[0]
                auflosung.append([x, y])
            j = j + 1
    return [hdmi, auflosung]


def read_WINEPREFIX():
    WINEPREFIX = "";
    if(debug_fodler != ""):
        WINEPREFIX = debug_fodler;
        os.system("mkdir -p \"" + debug_fodler + "/dosdevices" + "\"");
        return debug_fodler;
    try:
        WINEPREFIX = os.environ['WINEPREFIX'];
    except KeyError:
        home = os.environ['HOME'];
        WINEPREFIX = home + "/.wine";
    return WINEPREFIX;

def cancel():
    print("cancel..");
    exit();

def calulate_bigest_number(auflosung):
    out = [0, 0];
    for a1 in auflosung:
        auf1 = int(a1[0]);
        auf2 = int(a1[1]);
        if(out[0] < auf1 and out[1] < auf2):
            out[0] = auf1;
            out[1] = auf2;
    return out;

def main():
    auflosung_monitor = calulate_bigest_number(read_monitor_auflosung()[1]);
    print("Displayauflosung calulate: " + str(auflosung_monitor[0]) + "x" + str(auflosung_monitor[0]));
    WINEPREFIX = read_WINEPREFIX();
    if(len(sys.argv) == 2):
        wallpaper = sys.argv[1];
        if(os.path.isfile(wallpaper) == True):
            windowsdir = os.path.join(WINEPREFIX, "drive_c", "windows", "wallpaper.bmp");
            if(os.path.isfile(windowsdir) == True):
                i1 = input("delete the exist wallpaper[y,n]?");
                if(i1 == "y"):
                    os.system("/usr/bin/convert -scale " + str(auflosung_monitor[0]) + "x" + str(auflosung_monitor[0]) + " \"" + wallpaper +"\" " + "\"" + windowsdir + "\"");
                    #print("/usr/bin/convert \"" + wallpaper +"\" " + "\"" + windowsdir + "\"");
                    os.system("/usr/bin/wine64 regedit " + "\"" + reg_hak_file + "\"");
                    #print("/usr/bin/wine64 regedit " + "\"" + reg_hak_file + "\"");
                else:
                    cancel();
            else:
                if(True):
                    os.system("/usr/bin/convert \"" + wallpaper +"\" " + "\"" + windowsdir + "\"");
                    #print("/usr/bin/convert \"" + wallpaper +"\" " + "\"" + windowsdir + "\"");
                    os.system("/usr/bin/cp \"" + reg_hak_file + "\" " + windowsdir + ".reg");

                    os.system("/usr/bin/wine64 regedit " + "\"" + windowsdir + ".reg\"");
                    os.remove(windowsdir + ".reg");
                    #print("/usr/bin/wine64 regedit " + "\"" + reg_hak_file + "\"");
                else:
                    cancel();
    else:
        print("Wallpaper.bmp");
main();

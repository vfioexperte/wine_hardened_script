This is wine hardened script beta.
Protect a WINEPREFIX for not allowed access of your Devices.
See in the beta branch.


Installation:


„pip3.8 install pyqt5“

git clone https://github.com/vfioexperte/wine_hardened_script -b beta



usage:


Steam protect steam games:


how find a APPID?


protontricks  -s “Steam game name”


how start the program with  -Steam options.
Only use -Steam options for protontricks with this command. 


protontricks  -c "python3.8 '../wine_hardened_script_gui.py' -Steam" APPID

Proton protect auto:

protontricks  -c "python3.8 '../wine_hardened_script_gui.py' -Steam_auto_protect" APPID

Only use -Steam options for protontricks with this command. 


Proton remvoe protect auto:


protontricks  -c "python3.8 '../wine_hardened_script_gui.py' -Steam_auto_remove_protect" APPID

Only use -Steam options for protontricks with this command. 


wine Protect for  WINEPREFIX:


Step 1.


start the gui and click on „browse…“ and browse to your  WINEPREFIX folder.

Step 2.


the gui list alle wine device.

All True checkbox remove the path and create a dummy path. 
And protect the wine device for  not allowed access.

Stepp 3:


click on hardend start and the app apply all setings.

Start:

python3.8 '../wine_hardened_script_gui.py’


Protecion removeing:


click on the gui of remove hardened start.

This is a beta version.


Use at your risk.


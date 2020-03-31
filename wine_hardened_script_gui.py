#!/usr/bin/env python3.8
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP

version = "0.7f gui"
print(version);


from PyQt5 import QtWidgets
from PyQt5 import QtGui

import sys
import os
import os.path
import platform


steammode = 0;
steamauto = 0;
debug_fodler = "";
if(len(sys.argv) == 2):
    if(sys.argv[1] == "-Steam"):
        print("enabled Steam mode");
        print("use this mode only with protontricks command")
        print("you are find the APPID with protontricks -s \"game name\"");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam\" APPID")
        steammode = 1;
    elif(sys.argv[1] == "-Steam_auto_protect"):
        print("enabled Steam auto protect mode");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam_auto_protect\" APPID");
        print("auto protect mode enabled");
        steamauto = 1;
        steammode = 1;
    elif(sys.argv[1] == "-Steam_auto_remove_protect"):
        print("enabled Steam aurto remove protect mode");
        print("protontricks  -c \"python3.8 '/wine_hardened_script_gui.py' -Steam_auto_remove_protect\" APPID");
        print("auto remove protect mode enabled");
        steamauto = 2;
        steammode = 1;
    elif(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("options:");
        print("");
        print("-Steam");
        print("enabled Steam mode");
        print("use this mode only with protontricks command")
        print("you are find the APPID with protontricks -s \"game name\"");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam\" APPID")
        print("");
        print("Steam_auto_protect");
        print("enabled Steam auto protect mode");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' Steam_auto_protect\" APPID");
        print("auto protect mode enabled");
        print("");
        print("-Steam_auto_remove_protect");
        print("enabled Steam aurto remove protect mode");
        print("protontricks  -c \"python3.8 '/wine_hardened_script_gui.py' -Steam_auto_remove_protect\" APPID");
        print("auto remove protect mode enabled");
        print("");
        print("-debug");
        print("test debug folder");
        print("-debug /tmp");
        exit();
else:
    if(sys.argv[1] == "-debug"):
        debug_fodler = sys.argv[2];
        print("enable debug mode");

def system(cmd):
    os.system(cmd);

home = "";
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

def remnove_hardened(device, winefodler, block_output_folder):
    i = 0;
    while True:
        if(i >= len(device)):
            break;
        s2 = device[i];
        s1 = winefodler + "/" + s2 + ":";
        s3 = s1 + ":";
        #print("rm -f \"" + s1 + "\"");
        system("rm -f \"" + s1 + "\"");
        #print("rm -f \"" + s3 + "\"");
        system("rm -f \"" + s3 + "\"");
        i = i +1;

def add_hardened(device, winefodler, block_output_folder):
    remnove_hardened(device, winefodler, block_output_folder);
    i = 0;
    while True:
        if(i >= len(device)):
            break;
        if(device[i] != ","):
            s2 = device[i];
            s1 = winefodler + "/" + s2 + ":";
            #print("ln -sf " + "\"" + block_output_folder + "\" " + "\""  + s1 + "\"");
            system("ln -sf " + "\"" + block_output_folder + "\" " + "\""  + s1 + "\"");
        i = i +1;





def read_config_file(config):
    if(os.path.isfile(config) == False):
        return -1;
    file1 = open(config, "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    b1 = file1.read(size);
    file1.close();
    return b1;

def write_config_file(config, device_overide):
    file1 = open(config, "w");
    file1.write(device_overide)
    file1.close();
    return 0;

def restore_device_z(winefodler):
    s2 = winefodler + "/" + "z" + ":";
    #print("restore z:");
    os.system("ln -sf " + "/ " + "\"" + winefodler + "/z:" + "\"");
    return 0;

class Wine_hardened_script_gui(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.title = "Wine_hardened_script_gui - " + version;
        self.setWindowTitle(self.title);
        self.WINEPREFIX = read_WINEPREFIX();
        self.block_device = "a,b,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z";
        self.DEVICES = self.block_device.split(",");
        self.block_output_folder = "/tmp";
        self.device_overide = "";
        self.winefodler = self.WINEPREFIX + "/dosdevices"
        self.config = self.winefodler + "/.hardened.config";
        self.device_overide = "";
        self.mode = 0;

        self.layoutv1 = QtWidgets.QVBoxLayout(self)

        self.layouth1 = QtWidgets.QHBoxLayout()
        self.qlabel_wineprefix = QtWidgets.QLabel("WINEPREFIX:");
        self.textedit_wineprefix = QtWidgets.QTextEdit(self.WINEPREFIX);
        self.button_wineprefix = QtWidgets.QPushButton("browse..");
        self.button_wineprefix.clicked.connect(self.browse_WINEPREFIX);
        self.layouth1.addWidget(self.qlabel_wineprefix);
        self.layouth1.addWidget(self.textedit_wineprefix);
        self.layouth1.addWidget(self.button_wineprefix);
        self.layoutv1.addLayout(self.layouth1);
        self.bcolse = False;
	
        self.layouth2 = QtWidgets.QHBoxLayout()
        self.qlabel_a = QtWidgets.QLabel("a:");
        self.qlabel_a_tenner = QtWidgets.QLabel("->");
        self.qlabel_a_path = QtWidgets.QLabel("");
        self.qlabel_a_bool = QtWidgets.QCheckBox("");
        self.layouth2.addWidget(self.qlabel_a);
        self.layouth2.addWidget(self.qlabel_a_tenner);
        self.layouth2.addWidget(self.qlabel_a_path);
        self.layouth2.addWidget(self.qlabel_a_bool);

        self.layouth3 = QtWidgets.QHBoxLayout()
        self.qlabel_b = QtWidgets.QLabel("b:");
        self.qlabel_b_tenner = QtWidgets.QLabel("->");
        self.qlabel_b_path = QtWidgets.QLabel("");
        self.qlabel_b_bool = QtWidgets.QCheckBox("");
        self.layouth3.addWidget(self.qlabel_b);
        self.layouth3.addWidget(self.qlabel_b_tenner);
        self.layouth3.addWidget(self.qlabel_b_path);
        self.layouth3.addWidget(self.qlabel_b_bool);

        self.layouth4 = QtWidgets.QHBoxLayout()
        self.qlabel_c = QtWidgets.QLabel("c: disable");
        self.qlabel_c_tenner = QtWidgets.QLabel("->");
        self.qlabel_c_path = QtWidgets.QLabel("");
        self.qlabel_c_bool = QtWidgets.QCheckBox("");
        self.layouth4.addWidget(self.qlabel_c);
        self.layouth4.addWidget(self.qlabel_c_tenner);
        self.layouth4.addWidget(self.qlabel_c_path);
        self.layouth4.addWidget(self.qlabel_c_bool);

        self.layouth5 = QtWidgets.QHBoxLayout()
        self.qlabel_d = QtWidgets.QLabel("d:");
        self.qlabel_d_tenner = QtWidgets.QLabel("->");
        self.qlabel_d_path = QtWidgets.QLabel("");
        self.qlabel_d_bool = QtWidgets.QCheckBox("");
        self.layouth5.addWidget(self.qlabel_d);
        self.layouth5.addWidget(self.qlabel_d_tenner);
        self.layouth5.addWidget(self.qlabel_d_path);
        self.layouth5.addWidget(self.qlabel_d_bool);

        self.layouth6 = QtWidgets.QHBoxLayout()
        self.qlabel_e = QtWidgets.QLabel("e:");
        self.qlabel_e_tenner = QtWidgets.QLabel("->");
        self.qlabel_e_path = QtWidgets.QLabel("");
        self.qlabel_e_bool = QtWidgets.QCheckBox("");
        self.layouth6.addWidget(self.qlabel_e);
        self.layouth6.addWidget(self.qlabel_e_tenner);
        self.layouth6.addWidget(self.qlabel_e_path);
        self.layouth6.addWidget(self.qlabel_e_bool);

        self.layouth7 = QtWidgets.QHBoxLayout()
        self.qlabel_f = QtWidgets.QLabel("f:");
        self.qlabel_f_tenner = QtWidgets.QLabel("->");
        self.qlabel_f_path = QtWidgets.QLabel("");
        self.qlabel_f_bool = QtWidgets.QCheckBox("");
        self.layouth7.addWidget(self.qlabel_f);
        self.layouth7.addWidget(self.qlabel_f_tenner);
        self.layouth7.addWidget(self.qlabel_f_path);
        self.layouth7.addWidget(self.qlabel_f_bool);

        self.layouth8 = QtWidgets.QHBoxLayout()
        self.qlabel_g = QtWidgets.QLabel("g:");
        self.qlabel_g_tenner = QtWidgets.QLabel("->");
        self.qlabel_g_path = QtWidgets.QLabel("");
        self.qlabel_g_bool = QtWidgets.QCheckBox("");
        self.layouth8.addWidget(self.qlabel_g);
        self.layouth8.addWidget(self.qlabel_g_tenner);
        self.layouth8.addWidget(self.qlabel_g_path);
        self.layouth8.addWidget(self.qlabel_g_bool);


        self.layouth9 = QtWidgets.QHBoxLayout()
        self.qlabel_h = QtWidgets.QLabel("h:");
        self.qlabel_h_tenner = QtWidgets.QLabel("->");
        self.qlabel_h_path = QtWidgets.QLabel("");
        self.qlabel_h_bool = QtWidgets.QCheckBox("");
        self.layouth9.addWidget(self.qlabel_h);
        self.layouth9.addWidget(self.qlabel_h_tenner);
        self.layouth9.addWidget(self.qlabel_h_path);
        self.layouth9.addWidget(self.qlabel_h_bool);

        self.layouth10 = QtWidgets.QHBoxLayout()
        self.qlabel_i = QtWidgets.QLabel("i:");
        self.qlabel_i_tenner = QtWidgets.QLabel("->");
        self.qlabel_i_path = QtWidgets.QLabel("");
        self.qlabel_i_bool = QtWidgets.QCheckBox("");
        self.layouth10.addWidget(self.qlabel_i);
        self.layouth10.addWidget(self.qlabel_i_tenner);
        self.layouth10.addWidget(self.qlabel_i_path);
        self.layouth10.addWidget(self.qlabel_i_bool);

        self.layouth11 = QtWidgets.QHBoxLayout()
        self.qlabel_j = QtWidgets.QLabel("j:");
        self.qlabel_j_tenner = QtWidgets.QLabel("->");
        self.qlabel_j_path = QtWidgets.QLabel("");
        self.qlabel_j_bool = QtWidgets.QCheckBox("");
        self.layouth11.addWidget(self.qlabel_j);
        self.layouth11.addWidget(self.qlabel_j_tenner);
        self.layouth11.addWidget(self.qlabel_j_path);
        self.layouth11.addWidget(self.qlabel_j_bool);


        self.layouth12 = QtWidgets.QHBoxLayout()
        self.qlabel_k = QtWidgets.QLabel("k:");
        self.qlabel_k_tenner = QtWidgets.QLabel("->");
        self.qlabel_k_path = QtWidgets.QLabel("");
        self.qlabel_k_bool = QtWidgets.QCheckBox("");
        self.layouth12.addWidget(self.qlabel_k);
        self.layouth12.addWidget(self.qlabel_k_tenner);
        self.layouth12.addWidget(self.qlabel_k_path);
        self.layouth12.addWidget(self.qlabel_k_bool);


        self.layouth13 = QtWidgets.QHBoxLayout()
        self.qlabel_l = QtWidgets.QLabel("l:");
        self.qlabel_l_tenner = QtWidgets.QLabel("->");
        self.qlabel_l_path = QtWidgets.QLabel("");
        self.qlabel_l_bool = QtWidgets.QCheckBox("");
        self.layouth13.addWidget(self.qlabel_l);
        self.layouth13.addWidget(self.qlabel_l_tenner);
        self.layouth13.addWidget(self.qlabel_l_path);
        self.layouth13.addWidget(self.qlabel_l_bool);


        self.layouth14 = QtWidgets.QHBoxLayout()
        self.qlabel_m = QtWidgets.QLabel("m:");
        self.qlabel_m_tenner = QtWidgets.QLabel("->");
        self.qlabel_m_path = QtWidgets.QLabel("");
        self.qlabel_m_bool = QtWidgets.QCheckBox("");
        self.layouth14.addWidget(self.qlabel_m);
        self.layouth14.addWidget(self.qlabel_m_tenner);
        self.layouth14.addWidget(self.qlabel_m_path);
        self.layouth14.addWidget(self.qlabel_m_bool);

        self.layouth15 = QtWidgets.QHBoxLayout()
        self.qlabel_n = QtWidgets.QLabel("n:");
        self.qlabel_n_tenner = QtWidgets.QLabel("->");
        self.qlabel_n_path = QtWidgets.QLabel("");
        self.qlabel_n_bool = QtWidgets.QCheckBox("");
        self.layouth15.addWidget(self.qlabel_n);
        self.layouth15.addWidget(self.qlabel_n_tenner);
        self.layouth15.addWidget(self.qlabel_n_path);
        self.layouth15.addWidget(self.qlabel_n_bool);

        self.layouth16 = QtWidgets.QHBoxLayout()
        self.qlabel_o = QtWidgets.QLabel("o:");
        self.qlabel_o_tenner = QtWidgets.QLabel("->");
        self.qlabel_o_path = QtWidgets.QLabel("");
        self.qlabel_o_bool = QtWidgets.QCheckBox("");
        self.layouth16.addWidget(self.qlabel_o);
        self.layouth16.addWidget(self.qlabel_o_tenner);
        self.layouth16.addWidget(self.qlabel_o_path);
        self.layouth16.addWidget(self.qlabel_o_bool);

        self.layouth17 = QtWidgets.QHBoxLayout()
        self.qlabel_p = QtWidgets.QLabel("p:");
        self.qlabel_p_tenner = QtWidgets.QLabel("->");
        self.qlabel_p_path = QtWidgets.QLabel("");
        self.qlabel_p_bool = QtWidgets.QCheckBox("");
        self.layouth17.addWidget(self.qlabel_p);
        self.layouth17.addWidget(self.qlabel_p_tenner);
        self.layouth17.addWidget(self.qlabel_p_path);
        self.layouth17.addWidget(self.qlabel_p_bool);

        self.layouth18 = QtWidgets.QHBoxLayout()
        self.qlabel_q = QtWidgets.QLabel("q:");
        self.qlabel_q_tenner = QtWidgets.QLabel("->");
        self.qlabel_q_path = QtWidgets.QLabel("");
        self.qlabel_q_bool = QtWidgets.QCheckBox("");
        self.layouth18.addWidget(self.qlabel_q);
        self.layouth18.addWidget(self.qlabel_q_tenner);
        self.layouth18.addWidget(self.qlabel_q_path);
        self.layouth18.addWidget(self.qlabel_q_bool);

        self.layouth19 = QtWidgets.QHBoxLayout()
        self.qlabel_r = QtWidgets.QLabel("r:");
        self.qlabel_r_tenner = QtWidgets.QLabel("->");
        self.qlabel_r_path = QtWidgets.QLabel("");
        self.qlabel_r_bool = QtWidgets.QCheckBox("");
        self.layouth19.addWidget(self.qlabel_r);
        self.layouth19.addWidget(self.qlabel_r_tenner);
        self.layouth19.addWidget(self.qlabel_r_path);
        self.layouth19.addWidget(self.qlabel_r_bool);

        self.layouth20 = QtWidgets.QHBoxLayout()
        self.qlabel_s = QtWidgets.QLabel("s:");
        self.qlabel_s_tenner = QtWidgets.QLabel("->");
        self.qlabel_s_path = QtWidgets.QLabel("");
        self.qlabel_s_bool = QtWidgets.QCheckBox("");
        self.layouth20.addWidget(self.qlabel_s);
        self.layouth20.addWidget(self.qlabel_s_tenner);
        self.layouth20.addWidget(self.qlabel_s_path);
        self.layouth20.addWidget(self.qlabel_s_bool);

        self.layouth21 = QtWidgets.QHBoxLayout()
        self.qlabel_t = QtWidgets.QLabel("t:");
        self.qlabel_t_tenner = QtWidgets.QLabel("->");
        self.qlabel_t_path = QtWidgets.QLabel("");
        self.qlabel_t_bool = QtWidgets.QCheckBox("");
        self.layouth21.addWidget(self.qlabel_t);
        self.layouth21.addWidget(self.qlabel_t_tenner);
        self.layouth21.addWidget(self.qlabel_t_path);
        self.layouth21.addWidget(self.qlabel_t_bool);

        self.layouth22 = QtWidgets.QHBoxLayout()
        self.qlabel_u = QtWidgets.QLabel("u:");
        self.qlabel_u_tenner = QtWidgets.QLabel("->");
        self.qlabel_u_path = QtWidgets.QLabel("");
        self.qlabel_u_bool = QtWidgets.QCheckBox("");
        self.layouth22.addWidget(self.qlabel_u);
        self.layouth22.addWidget(self.qlabel_u_tenner);
        self.layouth22.addWidget(self.qlabel_u_path);
        self.layouth22.addWidget(self.qlabel_u_bool)

        self.layouth25 = QtWidgets.QHBoxLayout()
        self.qlabel_v = QtWidgets.QLabel("v:");
        self.qlabel_v_tenner = QtWidgets.QLabel("->");
        self.qlabel_v_path = QtWidgets.QLabel("");
        self.qlabel_v_bool = QtWidgets.QCheckBox("");
        self.layouth25.addWidget(self.qlabel_v);
        self.layouth25.addWidget(self.qlabel_v_tenner);
        self.layouth25.addWidget(self.qlabel_v_path);
        self.layouth25.addWidget(self.qlabel_v_bool)

        self.layouth26 = QtWidgets.QHBoxLayout()
        self.qlabel_w = QtWidgets.QLabel("w:");
        self.qlabel_w_tenner = QtWidgets.QLabel("->");
        self.qlabel_w_path = QtWidgets.QLabel("");
        self.qlabel_w_bool = QtWidgets.QCheckBox("");
        self.layouth26.addWidget(self.qlabel_w);
        self.layouth26.addWidget(self.qlabel_w_tenner);
        self.layouth26.addWidget(self.qlabel_w_path);
        self.layouth26.addWidget(self.qlabel_w_bool)

        self.layouth27 = QtWidgets.QHBoxLayout()
        self.qlabel_x = QtWidgets.QLabel("x:");
        self.qlabel_x_tenner = QtWidgets.QLabel("->");
        self.qlabel_x_path = QtWidgets.QLabel("");
        self.qlabel_x_bool = QtWidgets.QCheckBox("");
        self.layouth27.addWidget(self.qlabel_x);
        self.layouth27.addWidget(self.qlabel_x_tenner);
        self.layouth27.addWidget(self.qlabel_x_path);
        self.layouth27.addWidget(self.qlabel_x_bool)

        self.layouth28  = QtWidgets.QHBoxLayout()
        self.qlabel_y = QtWidgets.QLabel("y:");
        self.qlabel_y_tenner = QtWidgets.QLabel("->");
        self.qlabel_y_path = QtWidgets.QLabel("");
        self.qlabel_y_bool = QtWidgets.QCheckBox("");
        self.layouth28.addWidget(self.qlabel_y);
        self.layouth28.addWidget(self.qlabel_y_tenner);
        self.layouth28.addWidget(self.qlabel_y_path);
        self.layouth28.addWidget(self.qlabel_y_bool)


        self.layouth29 = QtWidgets.QHBoxLayout()
        self.qlabel_z = QtWidgets.QLabel("z:");
        self.qlabel_z_tenner = QtWidgets.QLabel("->");
        self.qlabel_z_path = QtWidgets.QLabel("");
        self.qlabel_z_bool = QtWidgets.QCheckBox("");
        self.layouth29.addWidget(self.qlabel_z);
        self.layouth29.addWidget(self.qlabel_z_tenner);
        self.layouth29.addWidget(self.qlabel_z_path);
        self.layouth29.addWidget(self.qlabel_z_bool)
        self.qlabel_z_dir = QtWidgets.QTextEdit("");
        if(steammode == 1):
            self.steammode = steammode;
            self.layouth29.addWidget(self.qlabel_z_dir);
            self.steamauto = steamauto;



        self.layoutv1.addLayout(self.layouth2);
        self.layoutv1.addLayout(self.layouth3);
        self.layoutv1.addLayout(self.layouth4);
        self.layoutv1.addLayout(self.layouth5);
        self.layoutv1.addLayout(self.layouth6);
        self.layoutv1.addLayout(self.layouth7);
        self.layoutv1.addLayout(self.layouth8);
        self.layoutv1.addLayout(self.layouth9);
        self.layoutv1.addLayout(self.layouth10);
        self.layoutv1.addLayout(self.layouth11);
        self.layoutv1.addLayout(self.layouth12);
        self.layoutv1.addLayout(self.layouth13);
        self.layoutv1.addLayout(self.layouth14);
        self.layoutv1.addLayout(self.layouth15);
        self.layoutv1.addLayout(self.layouth16);
        self.layoutv1.addLayout(self.layouth17);
        self.layoutv1.addLayout(self.layouth18);
        self.layoutv1.addLayout(self.layouth19);
        self.layoutv1.addLayout(self.layouth20);
        self.layoutv1.addLayout(self.layouth21);
        self.layoutv1.addLayout(self.layouth22);
        #self.layoutv1.addLayout(self.layouth23);
        #self.layoutv1.addLayout(self.layouth24);
        self.layoutv1.addLayout(self.layouth25);
        self.layoutv1.addLayout(self.layouth26);
        self.layoutv1.addLayout(self.layouth27);
        self.layoutv1.addLayout(self.layouth28);
        self.layoutv1.addLayout(self.layouth29);

        self.layouth30 = QtWidgets.QHBoxLayout()
        self.button_hardened = QtWidgets.QPushButton("start protection ");
        self.button_hardened.clicked.connect(self.hardened_start);
        self.button_remove_hardened = QtWidgets.QPushButton("remove protection start");
        self.button_remove_hardened.clicked.connect(self.remove_hardened);
        self.layouth30.addWidget(self.button_hardened);
        self.layouth30.addWidget(self.button_remove_hardened);
        self.layoutv1.addLayout(self.layouth30);

        self.textedit_wineprefix.setDisabled(True);
        self.change_WINEPREFIX(self.WINEPREFIX);

    def change_WINEPREFIX(self, wineprefix):
        if(os.path.isdir(wineprefix) == False):
            print("WINEPREFIX: " + "\"" + wineprefix + "\" not found!");
            exit();
        if(steammode != 0):
            if(wineprefix.find("compatdata") == -1 or wineprefix.find("pfx") == -1):
                print("WINEPREFIX: " + "\"" + wineprefix + "\" not a steam wine folder found!\nremove the -Steam options!");
                exit();
        self.WINEPREFIX = wineprefix;
        self.winefodler = self.WINEPREFIX + "/dosdevices"
        self.config = self.winefodler + "/.hardened.config";
        if(os.path.isfile(self.config) == True):
            self.mode = 1;
            self.button_hardened.setDisabled(True);
            self.button_remove_hardened.setDisabled(False);
        else:
            self.mode = 0;
            self.button_hardened.setDisabled(False);
            self.button_remove_hardened.setDisabled(True);
        self.change_gui(self.block_device, self.winefodler);
        return 0;

    def change_gui(self, block_device, winefodler):
        self.steamauto = steamauto;
        self.steammode = steammode;
        device = block_device.split(",");
        if(self.mode == 1):
                if(os.path.isfile(self.config) == True):
                    self.device_overide = read_config_file(self.config);
                    self.set_cheboxes(self.device_overide, self.block_device);
                    return 0;
        device_overide = "";
        i = 0;
        while True:
                if(i >= len(device)):
                        break;
                s2 = device[i];
                s1 = winefodler + "/" + s2 + ":";
                if(os.path.islink(s1) == True):
                    device_overide = device_overide + "0" + ",";
                elif(os.path.islink(s1+":") == True):
                    device_overide = device_overide + "0" + ",";
                else:
                    device_overide = device_overide + "1" + ",";

                i = i +1;
        self.set_cheboxes(device_overide, self.block_device);
        return 0;

    def set_cheboxes(self, device_overide, block_device2):
        block_device = block_device2.split(",");
        #self.block_device
        stext = "";
        self.device_overide = device_overide;
        device_overide = device_overide.split(",");
        if(self.mode == 0):
            stext = "create a protection device ";
        else:
            stext = "remove a protection device ";

        if(device_overide[0] == "0"):
            self.qlabel_a_bool.setDisabled(False);
            self.qlabel_a_bool.setText(stext + block_device[0]);
            self.qlabel_a_bool.setChecked(False);
        else:
            self.qlabel_a_bool.setDisabled(True);
            self.qlabel_a_bool.setText(stext + block_device[0]);
            self.qlabel_a_bool.setChecked(True);

        if(device_overide[1] == "0"):
            self.qlabel_b_bool.setDisabled(False);
            self.qlabel_b_bool.setText(stext + block_device[1]);
            self.qlabel_b_bool.setChecked(False);
        else:
            self.qlabel_b_bool.setDisabled(True);
            self.qlabel_b_bool.setText(stext + block_device[1]);
            self.qlabel_b_bool.setChecked(True);

        if(device_overide[2] == "0"):
            self.qlabel_d_bool.setDisabled(False);
            self.qlabel_d_bool.setText(stext + block_device[2]);
            self.qlabel_d_bool.setChecked(False);
        else:
            self.qlabel_d_bool.setDisabled(True);
            self.qlabel_d_bool.setText(stext + block_device[2]);
            self.qlabel_d_bool.setChecked(True);

        if(device_overide[3] == "0"):
            self.qlabel_e_bool.setDisabled(False);
            self.qlabel_e_bool.setText(stext + block_device[3]);
            self.qlabel_e_bool.setChecked(False);
        else:
            self.qlabel_e_bool.setDisabled(True);
            self.qlabel_e_bool.setText(stext + block_device[3]);
            self.qlabel_e_bool.setChecked(True);

        if(device_overide[4] == "0"):
            self.qlabel_f_bool.setDisabled(False);
            self.qlabel_f_bool.setText(stext + block_device[4]);
            self.qlabel_f_bool.setChecked(False);
        else:
            self.qlabel_f_bool.setDisabled(True);
            self.qlabel_f_bool.setText(stext + block_device[4]);
            self.qlabel_f_bool.setChecked(True);

        if(device_overide[5] == "0"):
            self.qlabel_g_bool.setDisabled(False);
            self.qlabel_g_bool.setText(stext + block_device[5]);
            self.qlabel_g_bool.setChecked(False);
        else:
            self.qlabel_g_bool.setDisabled(True);
            self.qlabel_g_bool.setText(stext + block_device[5]);
            self.qlabel_g_bool.setChecked(True);

        if(device_overide[6] == "0"):
            self.qlabel_h_bool.setDisabled(False);
            self.qlabel_h_bool.setText(stext + block_device[6]);
            self.qlabel_h_bool.setChecked(False);
        else:
            self.qlabel_h_bool.setDisabled(True);
            self.qlabel_h_bool.setText(stext + block_device[6]);
            self.qlabel_h_bool.setChecked(True);

        if(device_overide[7] == "0"):
            self.qlabel_i_bool.setDisabled(False);
            self.qlabel_i_bool.setText(stext + block_device[7]);
            self.qlabel_i_bool.setChecked(False);
        else:
            self.qlabel_i_bool.setDisabled(True);
            self.qlabel_i_bool.setText(stext + block_device[7]);
            self.qlabel_i_bool.setChecked(True);

        if(device_overide[8] == "0"):
            self.qlabel_j_bool.setDisabled(False);
            self.qlabel_j_bool.setText(stext + block_device[8]);
            self.qlabel_j_bool.setChecked(False);
        else:
            self.qlabel_j_bool.setDisabled(True);
            self.qlabel_j_bool.setText(stext + block_device[8]);
            self.qlabel_j_bool.setChecked(True);

        if(device_overide[9] == "0"):
            self.qlabel_k_bool.setDisabled(False);
            self.qlabel_k_bool.setText(stext + block_device[9]);
            self.qlabel_k_bool.setChecked(False);
        else:
            self.qlabel_k_bool.setDisabled(True);
            self.qlabel_k_bool.setText(stext + block_device[9]);
            self.qlabel_k_bool.setChecked(True);

        if(device_overide[10] == "0"):
            self.qlabel_l_bool.setDisabled(False);
            self.qlabel_l_bool.setText(stext + block_device[10]);
            self.qlabel_l_bool.setChecked(False);
        else:
            self.qlabel_l_bool.setDisabled(True);
            self.qlabel_l_bool.setText(stext + block_device[10]);
            self.qlabel_l_bool.setChecked(True);

        if(device_overide[11] == "0"):
            self.qlabel_m_bool.setDisabled(False);
            self.qlabel_m_bool.setText(stext + block_device[11]);
            self.qlabel_m_bool.setChecked(False);
        else:
            self.qlabel_m_bool.setDisabled(True);
            self.qlabel_m_bool.setText(stext + block_device[11]);
            self.qlabel_m_bool.setChecked(True);

        if(device_overide[12] == "0"):
            self.qlabel_n_bool.setDisabled(False);
            self.qlabel_n_bool.setText(stext + block_device[12]);
            self.qlabel_n_bool.setChecked(False);
        else:
            self.qlabel_n_bool.setDisabled(True);
            self.qlabel_n_bool.setText(stext + block_device[12]);
            self.qlabel_n_bool.setChecked(True);

        if(device_overide[13] == "0"):
            self.qlabel_o_bool.setDisabled(False);
            self.qlabel_o_bool.setText(stext + block_device[13]);
            self.qlabel_o_bool.setChecked(False);
        else:
            self.qlabel_o_bool.setDisabled(True);
            self.qlabel_o_bool.setText(stext + block_device[13]);
            self.qlabel_o_bool.setChecked(True);

        if(device_overide[14] == "0"):
            self.qlabel_p_bool.setDisabled(False);
            self.qlabel_p_bool.setText(stext + block_device[14]);
            self.qlabel_p_bool.setChecked(False);
        else:
            self.qlabel_p_bool.setDisabled(True);
            self.qlabel_p_bool.setText(stext + block_device[14]);
            self.qlabel_p_bool.setChecked(True);

        if(device_overide[15] == "0"):
            self.qlabel_q_bool.setDisabled(False);
            self.qlabel_q_bool.setText(stext + block_device[15]);
            self.qlabel_q_bool.setChecked(False);
        else:
            self.qlabel_q_bool.setDisabled(True);
            self.qlabel_q_bool.setText(stext + block_device[15]);
            self.qlabel_q_bool.setChecked(True);

        if(device_overide[16] == "0"):
            self.qlabel_r_bool.setDisabled(False);
            self.qlabel_r_bool.setText(stext + block_device[16]);
            self.qlabel_r_bool.setChecked(False);
        else:
            self.qlabel_r_bool.setDisabled(True);
            self.qlabel_r_bool.setText(stext + block_device[16]);
            self.qlabel_r_bool.setChecked(True);

        if(device_overide[17] == "0"):
            self.qlabel_s_bool.setDisabled(False);
            self.qlabel_s_bool.setText(stext + block_device[17]);
            self.qlabel_s_bool.setChecked(False);
        else:
            self.qlabel_s_bool.setDisabled(True);
            self.qlabel_s_bool.setText(stext + block_device[17]);
            self.qlabel_s_bool.setChecked(True);

        if(device_overide[18] == "0"):
            self.qlabel_t_bool.setDisabled(False);
            self.qlabel_t_bool.setText(stext + block_device[18]);
            self.qlabel_t_bool.setChecked(False);
        else:
            self.qlabel_t_bool.setDisabled(True);
            self.qlabel_t_bool.setText(stext + block_device[18]);
            self.qlabel_t_bool.setChecked(True);

        if(device_overide[19] == "0"):
            self.qlabel_u_bool.setDisabled(False);
            self.qlabel_u_bool.setText(stext + block_device[19]);
            self.qlabel_u_bool.setChecked(False);
        else:
            self.qlabel_u_bool.setDisabled(True);
            self.qlabel_u_bool.setText(stext + block_device[19]);
            self.qlabel_u_bool.setChecked(True);

        if(device_overide[20] == "0"):
            self.qlabel_v_bool.setDisabled(False);
            self.qlabel_v_bool.setText(stext + block_device[20]);
            self.qlabel_v_bool.setChecked(False);
        else:
            self.qlabel_v_bool.setDisabled(True);
            self.qlabel_v_bool.setText(stext + block_device[20]);
            self.qlabel_v_bool.setChecked(True);

        if(device_overide[21] == "0"):
            self.qlabel_w_bool.setDisabled(False);
            self.qlabel_w_bool.setText(stext + block_device[21]);
            self.qlabel_w_bool.setChecked(False);
        else:
            self.qlabel_w_bool.setDisabled(True);
            self.qlabel_w_bool.setText(stext + block_device[21]);
            self.qlabel_w_bool.setChecked(True);

        if(device_overide[22] == "0"):
            self.qlabel_x_bool.setDisabled(False);
            self.qlabel_x_bool.setText(stext + block_device[22]);
            self.qlabel_x_bool.setChecked(False);
        else:
            self.qlabel_x_bool.setDisabled(True);
            self.qlabel_x_bool.setText(stext + block_device[22]);
            self.qlabel_x_bool.setChecked(True);

        if(device_overide[23] == "0"):
            self.qlabel_y_bool.setDisabled(False);
            self.qlabel_y_bool.setText(stext + block_device[23]);
            self.qlabel_y_bool.setChecked(False);
        else:
            self.qlabel_y_bool.setDisabled(True);
            self.qlabel_y_bool.setText(stext + block_device[23]);
            self.qlabel_y_bool.setChecked(True);

        if(device_overide[24] == "0" and self.mode == 0):
            self.qlabel_z_bool.setDisabled(False);
            self.qlabel_z_bool.setText(stext + block_device[24]);
            self.qlabel_z_bool.setChecked(False);
            if(self.steammode == 1):
                s1  = self.textedit_wineprefix.toPlainText();
                s1 = os.path.realpath(s1+"../../../../");
                self.qlabel_z_dir.setText(s1);
                self.qlabel_z_bool.setText("create a protection device path ->");
                self.qlabel_z_dir.setHidden(False);
                self.qlabel_z_dir.setDisabled(False);
                if(self.steamauto == 1):
                    self.qlabel_z_bool.setChecked(True);
            else:
                self.qlabel_z_dir.setHidden(True);
        else:
            self.qlabel_z_bool.setDisabled(False);
            self.qlabel_z_bool.setText("resore a protection device " + block_device[24]);
            self.qlabel_z_bool.setChecked(False);
            self.qlabel_z_dir.setText("");
            self.qlabel_z_dir.setDisabled(True);
            self.qlabel_z_dir.setHidden(True);
            if(self.steamauto == 2):
                self.qlabel_z_bool.setChecked(True);

        self.qlabel_c_bool.setDisabled(True);
        self.qlabel_c_bool.setText(stext + "c");
        self.qlabel_c_bool.setChecked(False);
        app.processEvents();
        return 0;




    def calculate1(self):
        device = "";
        device_overide = "";
        if(self.qlabel_a_bool.isChecked() == True):
            device = device + "a" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_b_bool.isChecked() == True):
            device = device + "b" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_d_bool.isChecked() == True):
            device = device + "d" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_e_bool.isChecked() == True):
            device = device + "e" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_f_bool.isChecked() == True):
            device = device + "f" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_g_bool.isChecked() == True):
            device = device + "g" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_h_bool.isChecked() == True):
            device = device + "h" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_i_bool.isChecked() == True):
            device = device + "i" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_j_bool.isChecked() == True):
            device = device + "j" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_k_bool.isChecked() == True):
            device = device + "k" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_l_bool.isChecked() == True):
            device = device + "l" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_m_bool.isChecked() == True):
            device = device + "m" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_n_bool.isChecked() == True):
            device = device + "n" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_o_bool.isChecked() == True):
            device = device + "o" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_p_bool.isChecked() == True):
            device = device + "p" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_q_bool.isChecked() == True):
            device = device + "q" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_r_bool.isChecked() == True):
            device = device + "r" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_s_bool.isChecked() == True):
            device = device + "s" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_t_bool.isChecked() == True):
            device = device + "t" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_u_bool.isChecked() == True):
            device = device + "u" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_v_bool.isChecked() == True):
            device = device + "v" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_w_bool.isChecked() == True):
            device = device + "w" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_x_bool.isChecked() == True):
            device = device + "x" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_y_bool.isChecked() == True):
            device = device + "y" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";

        if(self.qlabel_z_bool.isChecked() == True):
            device = device + "z" + ",";
            device_overide = device_overide + "1" + ",";
        else:
            device_overide = device_overide + "0" + ",";
        #print(self.device_overide)
        #print(device_overide);
        self.device_overide = device_overide;
        return device;

    def hardened_start(self):
        if(os.path.isfile(self.config) == True):
            print("ERROR is protect");
            exit();
        self.DEVICES = self.calculate1();
        print(self.DEVICES);
        remnove_hardened(self.DEVICES, self.winefodler, self.block_output_folder);
        add_hardened(self.DEVICES, self.winefodler, self.block_output_folder);
        write_config_file(self.config, self.device_overide);
        if(self.steammode == 1):
            s1 = self.qlabel_z_dir.toPlainText();
            s2 = self.winefodler + "/" + "z" + ":";
            os.system("rm -f " + "\"" + s2  +  "\"");
            os.system("ln -sf " + s1 + " " + "\"" + s2  +  "\"" );

        self.change_WINEPREFIX(self.WINEPREFIX);
        self.change_gui(self.block_device, self.winefodler);
        return 0;
    def remove_hardened(self):
        if(os.path.isfile(self.config) == False):
            print("ERROR is not protect please run protection first");
            exit();
        self.DEVICES = self.calculate1();
        remnove_hardened(self.DEVICES, self.winefodler, self.block_output_folder);
        os.system("rm -f " + self.config);
        if(self.qlabel_z_bool.isChecked() == True):
            restore_device_z(self.winefodler);

        self.change_WINEPREFIX(self.WINEPREFIX);
        self.change_gui(self.block_device, self.winefodler);
        return 0;
    def browse_WINEPREFIX(self):            
        msgBox = QtWidgets.QMessageBox();
        msgBox.setIcon(QtWidgets.QMessageBox.Warning);
        if(self.steammode == 1):
            self.steammode = 0;
            msgBox.setText("You are in steamode and disabled steammode");
            msgBox.exec();
        while True:
            fieldialog = QtWidgets.QFileDialog;
            file = fieldialog.getExistingDirectory(self, "WINEPREFIX", home);
            if(file == ""):
                exit();
            if(os.path.exists(file + "/dosdevices")  == True):
                self.textedit_wineprefix.setText(file);
                self.change_WINEPREFIX(file);
                self.textedit_wineprefix.setText(file);
                self.change_gui(self.block_device, self.winefodler);
                break;
            else:
                msgBox.setText("The folder isn't a WINEPREFIX: \"" + file + "\"");
                msgBox.exec();
        return 0;

    def closeEvent(self, event):
        self.bcolse = True;
        event.accept();
    def calculate_path1(self, path):
        i = len(path);
        badd = 0;
        b1 = 0;
        while True:
            if(i == 0):
                break;
            if(path[i] == '/'):
                badd = badd + 1;
            if(badd >= 5):
                b1 = 1;
                break;
            i = i -1;
        j = 0;
        s1 = "";
        while True:
            if(j >= i):
                break;
            if(j >= len(path)):
                break;
            s1 = s1 + path[j];
            j = j +1;
        return s1;

app = QtWidgets.QApplication(sys.argv);
mainwindow = Wine_hardened_script_gui();
mainwindow.show();
if(steamauto == 1):
    mainwindow.hardened_start();
    mainwindow.close();
elif(steamauto == 2):
    mainwindow.remove_hardened();
    mainwindow.close();
else:
    app.exec_();


#!/usr/bin/env python
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
version = "0.3a"
print(version);

import sys
import os
import os.path
import platform
import string

mode = 0;

appname = "wine-no-internet";
tmpfile = "/tmp/wine-no-internet.tmp";

config = "/etc/" + appname;

def liste_alles_users_auf():
    os.system("cut -d: -f1 /etc/passwd "  + " >"+ tmpfile + ".2");
    file1 = open(tmpfile + ".2", "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    s1 = file1.read(size);
    file1.close();

    s2 = s1.split("\n");
    users = [];

    i = 0;
    while True:
        if(i >= len(s2)):
            break;
        if(check_user_add_goup(s2[i], "users") == 1):
            if(check_user_aht_eine_home_verzeichnis(s2[i]) == 1):
                users.append(s2[i]);
        i =  i +1;
    print(users);
    os.remove(tmpfile + ".2");
    return users;

def check_user_aht_eine_home_verzeichnis(user):
    os.system("ls /home/ " + " >"+ tmpfile + ".1");
    file1 = open(tmpfile + ".1", "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    s1 = file1.read(size);
    file1.close();
    s2 = s1.split("\n");
    #print(s2)
    #print(len(s2));
    i = 0;
    while True:
        if(i >= len(s2)):
            break;
        if(s2[i] == user):
            os.remove(tmpfile + ".1");
            return 1;
        i = i +1;
    os.remove(tmpfile + ".1");
    return 0;




def check_user_add_goup(user, group):
    os.system("groups " +user + " >"+ tmpfile);
    file1 = open(tmpfile, "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    s1 = file1.read(size);
    file1.close();
    s2 = s1.split(" ");
    #print(s2)
    #print(len(s2));
    i = 0;
    while True:
        if(i >= len(s2)):
            break;
        if(s2[i].find(group) != 0):
            os.remove(tmpfile);
            return 1;
        i = i +1;
    os.remove(tmpfile);
    return 0;


def exit_():
    if(os.path.isfile(tmpfile) == True):
        os.remove(tmpfile);
    exit();

def main():
    if(len(sys.argv) == 2):
        if(sys.argv[1] == "-check"):
            if(os.path.isfile(config) == True):
                user = os.environ['USER'];
                if(check_user_add_goup(user, "no-internet") == 0):
                    os.system("usermod -aG no-internet " + user);
                    print("user: " + user + " add group no-internet");
                    print(appname + " is install");
                    if(check_user_add_goup(user, "no-internet") == 0):
                        print("no root acces");
                    else:
                        exit_();
                else:
                    exit_();

    if(os.path.isfile(config) == False):
        #creat
        os.system("groupadd no-internet");
        print("create a firwall");
        os.system("iptables -I OUTPUT 1 -m owner --gid-owner no-internet -j DROP");
        os.system("ip6tables -I OUTPUT 1 -m owner --gid-owner no-internet -j DROP");
        os.system("iptables-save");

        os.system("users " + " >"+ tmpfile);
        file1 = open(tmpfile, "r");
        file1.seek(0, 2);
        size = file1.tell();
        file1.seek(0, 0);
        s1 = file1.read(size);
        file1.close();



        frage2 = input("add all user [y,n]: ");
        if(frage2 == "y"):
            print("y");
            i = 0;
            s2 = liste_alles_users_auf();
            print(len(s2));
            while True:
                if(i >= len(s2)):
                    break;
                user = s2[i];
                os.system("usermod -aG no-internet " + user);
                print("add user: " + user);
                i = i +1;
        file1 = open(config, "w");
        file1.write("1");
        file1.close();
        print("create");
        exit_();
    else:
        #remove
        frage = input("remove wine-no-internet configs[y,n]: ");
        if(frage == "y"):
            os.system("iptables -F");
            os.system("iptables -XF");
            os.system("iptables -t nat -F");
            os.system("iptables -t nat -X");
            os.system("iptables -t mangle -F");
            os.system("iptables -t mangle -X");
            os.system("iptables -P INPUT ACCEPT");
            os.system("iptables -P FORWARD ACCEPT");
            os.system("iptables -P OUTPUT ACCEPT");

            os.system("ip6tables -F");
            os.system("ip6tables -XF");
            os.system("ip6tables -t nat -F");
            os.system("ip6tables -t nat -X");
            os.system("ip6tables -t mangle -F");
            os.system("ip6tables -t mangle -X");
            os.system("ip6tables -P INPUT ACCEPT");
            os.system("ip6tables -P FORWARD ACCEPT");
            os.system("ip6tables -P OUTPUT ACCEPT");

            os.system("groupdel no-internet");
            os.remove(config)
            print("remove");
            exit_();
        else:
           print("exit");
           exit_();

main();

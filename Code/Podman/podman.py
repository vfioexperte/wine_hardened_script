import platform
import os
import sys
import string
import subprocess
import time
import threading

version = "0.1c"

def read_file_string(s1):
    f1 = open(s1, "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    out = f1.read(size);
    f1.close();
    return out;

def system(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True).decode().split("\n");
        return output;
    except subprocess.CalledProcessError:
        return "";
    except FileNotFoundError:
        return "";

def podman_find_network_bridge(bridgename, out):
    for tmp in out:
        tmp2 = tmp.split();
        if(len(tmp2) >= 2):
            if(tmp2[1] == bridgename):
                return tmp2[0]
    return "";

def podman_network_array_to_gateway_ip(out):
    b1 = 0;
    for tmp in out:
        tmp2 = tmp.split();
        for tmp3 in tmp2:
            if(b1 == 1):
                return tmp3.split("\"")[1];
            if(tmp3 == "\"gateway\":"):
                b1 = 1;
    return "";


def podman_network_bridge_find_gateway(bridge_name, podman_als_root):
    cmd = "";
    if(podman_als_root == 1):
        cmd = "sudo "
    out = system(cmd + "podman network ls");
    id = podman_find_network_bridge(bridge_name, out);
    if(id == ""):
        print("bridge name not found!");
        return "";
    out = system(cmd + "podman network inspect " +  id);
    ip = podman_network_array_to_gateway_ip(out);
    return ip


def pacman_list_a_downlaod_pkg(basename):
    if(basename == "system_only" or basename == "system_only2" or basename == "command_root_docker" or basename == "login"  or basename == "login_root" or basename == "command" or basename == "command_root" or basename == "command_root_docker" or basename == "edit_config" ):
        return [];
    os.system("./command_root_docker 'pacman -Sy && pacman -Ss' >pipe.tmp");
    out1 = read_file_string("pipe.tmp").split("\n")
    #out1 = system("pacman -Ss");
    out = [];
    for tmp in out1:
        tmp2 = tmp.split();
        if(len(tmp2) < 1):
            continue;
        if(tmp2[0].find("/") != -1):
            out.append(tmp2[0].split("/")[1])
    return out;

def check_array_pacman_pkg_exist(out, string):
    a2 = string.split();
    out2 = "";
    failed = [];
    print(a2)
    for tmp in a2:
        b1 = 0;
        for tmp2 in out:
            if(tmp2 == tmp):
                out2 = out2 + " " + tmp;
                b1 = 1;
        if(b1 == 0):
            failed.append(tmp);
    return [out2, failed];

def check_array_gamecope(a1, a2):
    if(len(a1) == 0):
        if(len(a2) != 0):
            return a2;
        else:
            return [];
    if(len(a2) == 0):
        if(len(a1) != 0):
            return a1;
        else:
            return [];
    windowids = [];
    for tmp in a1:
        b1 = 0;
        for tmp2 in a2:
            if(tmp == tmp2):
                b1 = 1;
                break;
        if(b1 == 0):
            windowids.append(tmp);
    for tmp in a2:
        b1 = 0;
        for tmp2 in a1:
            if(tmp == tmp2):
                b1 = 1;
                break;
        if(b1 == 0):
            windowids.append(tmp);
    return windowids;



def list_all_ids():
    out = [];
    cmd = system("xwininfo -root -children -all")
    for tmp in cmd:
        tmp2 = tmp.split();
        if(len(tmp2) >= 4):
            if(tmp2[0] == "xwininfo:"):
                continue;
            elif(tmp2[0] == "Root"):
                continue;
            elif(tmp2[0] == "Parent"):
                continue;
            else:
                out.append(tmp2[0]);
                continue;
    return out;

def gamescope_not_used(docker_build, docker_system, podman_runs_root):
    #v0.2a
    if(docker_build.find("localhost/") != -1):
        docker_build = docker_build.split("localhost/")[1]
    cmd = "";
    for tmp in sys.argv[::-1][:-1][::-1]:
        if(tmp.find(" ") != -1):
            cmd = cmd + " \"" + tmp + "\" ";
        else:
            cmd = cmd + " " + tmp + " ";
    while True:
        if(os.path.isfile("/tmp/gamscope.lock") == False):
            break;
    os.system("echo 1 >/tmp/gamscope.lock");
    gamescope_ids = gamescope_to_window_id_x11();
    th1 = start_thread(cmd);
    gamescope_ids2 = "";
    while True:
        gamescope_ids2 = gamescope_to_window_id_x11();
        ids = check_array_gamecope(gamescope_ids2, gamescope_ids);
        if(len(ids) >= 1):
            break;
        #time.sleep(0.25);
    time.sleep(8);
    dockerid = read_docker_ps(docker_build, docker_system, podman_runs_root)
    ids = check_array_gamecope(gamescope_ids2, gamescope_ids);
    os.system("sudo rm /tmp/gamscope.lock");
    while True:
        gamescope_ids2 = gamescope_to_window_id_x11();
        ids = check_array_gamecope(gamescope_ids2, gamescope_ids);
        if(len(ids) >= 1):
            break;
        #time.sleep(0.25);
    if(len(ids) == 0):
        exit(-1)
    while True:
        allids = list_all_ids();
        b1 = 0;
        for tmp in allids:
            if(tmp == ids[len(ids) - 1]):
                b1 = 1;
        if(b1 == 0):
            break;
        time.sleep(0.25);
    #exit();
    if(docker_system == 1):
        #docker
        s1 = "docker stop " + dockerid;
        print(s1)
        os.system(s1);
        s1 = "docker kill " + dockerid;
        os.system(s1);
    elif(podman_runs_root == 0):
        if(docker_system == 2):
            #podman
            s1 = "podman stop " + dockerid;
            print(s1)
            os.system(s1);
            s1 = "podman kill " + dockerid;
            os.system(s1);
    else:
        if(docker_system == 2):
            #podman
            s1 = "sudo podman stop " + dockerid;
            print(s1)
            os.system(s1);
            s1 = "sudo podman kill " + dockerid;
            os.system(s1);
    #os.system("clear")
    return 0;

class cmd_thread(threading.Thread):
    def __init__(self):
        super(cmd_thread, self).__init__()
        self.total=0
    def set(self, cmd):
        self.cmd = cmd;
        self.exit = 0;
        return 0;
    def run(self):
        #system(self.cmd);
        #cmd = subprocess.check_output(self.cmd, shell=True).decode();
        os.system(self.cmd);
        #print(cmd);
        self.exit = 1;
    def exit(self):
        return self.exit;

def start_thread(cmd):
    thread = cmd_thread();
    thread.set(cmd);
    thread.start();
    return thread;


def podman_check_stati_ip(static_ip, gateway_ip):
    tmp = [];
    if(len(static_ip.split(".")) >= 4):
        tmp = static_ip.split(".")
    tmp2 = gateway_ip.split(".")
    if(len(tmp) == 0):
        return [];
    if(gateway_ip == ""):
        return [];
    b1 = 0;
    if(tmp[0] == tmp2[0]):
        if(tmp[1] == tmp2[1]):
            if(tmp[2] == tmp2[2]):
                b1 = 1;
    if(b1 == 1):
        return static_ip;
    s1 = tmp2[0] + "." + tmp2[1] + "." + tmp2[2] + "." + tmp[3];
    return s1;

def podman_pkg_doppelt_check(s1):
    a1 = s1.split();
    print(a1)
    out = [];
    for tmp in a1:
        b1 = 0;
        for tmp2 in out:
            if(tmp2 == tmp):
                b1 = 1;
                break;
        if(b1 == 0):
            out.append(tmp);
    s1 = "";
    for tmp in out:
        s1 = s1 + tmp + " ";
    return s1;

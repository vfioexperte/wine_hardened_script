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

mode = 0;

appname = "wine-to-docker";
pulse_config = "/usr/share/wine-security-gui/pulse-client.conf"
dcokerfile = "/usr/share/wine-security-gui/Dockerfile"
buildfile = "/usr/share/wine-security-gui/build"
user = "wine";
gpu_reader = 0;


def input_name():
    i1 = input("Name des docker wine containers?: ");
    return i1;


def create_Dockerfile(docker_container_name):
    os.system("mkdir -p \"" + docker_container_name + "/src" +  "\"");
    python_dockerfile1 = "FROM archlinux/base\n\n";
    python_dockerfile1_2 = "#" +  version + "_create_with_" + appname + "\n";
    python_dockerfile1 = python_dockerfile1  + python_dockerfile1_2;
    python_dockerfile2 = "RUN echo \"[multilib]\" >>/etc/pacman.conf\n";
    python_dockerfile3 = "RUN echo \"Include = /etc/pacman.d/mirrorlist\" >>/etc/pacman.conf\n";
    python_dockerfile4 = "RUN pacman -Sy archlinux-keyring --noconfirm -y\n";
    python_dockerfile5 = "RUN pacman -Syu base base-devel xf86-video-ati xf86-video-amdgpu  xorg xorg-server xorg-xinit mesa-demos vulkan-tools  vulkan-mesa-layers vulkan-radeon  vulkan-icd-loader pulseaudio alsa-tools alsa-utils pulseaudio-alsa pavucontrol  wine lib32-mpg123 openra winetricks openal firefox-i18n-de xfce4-terminal openvpn dotnet-runtime dotnet-sdk thunar ntfs-3g exfat-utils --noconfirm -y \n";
    python_dockerfile6 = "RUN useradd -m -g users -G video,audio,wheel " + user + " \n";
    python_dockerfile7 = "CMD steam\n";

    f1 = open(docker_container_name + "/src/Dockerfile", "w");
    f1.write(python_dockerfile1);
    f1.write(python_dockerfile2);
    f1.write(python_dockerfile3);
    f1.write(python_dockerfile4);
    f1.write(python_dockerfile5);
    f1.write(python_dockerfile6);
    f1.write(python_dockerfile7);
    f1.close();
    return 0;

def configure_build_file(docker_container_name):
    file1 = open(docker_container_name + "/.config", "w");
    username = input("your docker user name: ");
    if(username == ""):
        username = "empty";
    file1.write("docker_user = " + username + "\n");
    gpurender = input("GPU render DRI_PRIME 1-99: ");
    if(gpurender == ""):
        gpurender = "1";
    file1.write("gpu_render = " + gpurender + "\n");
    file1.write("disk_device_name = cd/dvd\n");
    zugriff_auf_media = input("Allow to acces docker container /run/media y,n? ");
    if(zugriff_auf_media == "y"):
        file1.write("zugriff_auf_media = 1\n");
    if(zugriff_auf_media == "n"):
        file1.write("zugriff_auf_media = 0\n");

    sav_home_docker_folder = input("Allow to sav the home folder in docker container y,n? ");
    if(sav_home_docker_folder == "y"):
        file1.write("sav_home_docker_folder = 1\n");
    if(sav_home_docker_folder == "n"):
        file1.write("sav_home_docker_folder = 0\n");

    share_folder_daten = input("create a share fodler daten y,n? ");
    if(share_folder_daten == "y"):
        file1.write("share_folder_daten = 1\n");
    if(share_folder_daten == "n"):
        file1.write("share_folder_daten = 0\n");

    custom_sharefodler_bool = input("create a share custom fodler daten y,n? ");
    if(custom_sharefodler_bool == "y"):
        custom_sharefodler_path = input("The custom share fodler path: ");
        if(custom_sharefodler_path != ""):
            file1.write("share_folder1_aktiv = 1\n");
            file1.write("share_folder1 = " + custom_sharefodler_path + "\n");
    if(custom_sharefodler_bool == "n"):
        file1.write("share_folder1_aktiv = 0\n");
        file1.write("share_folder1 = " + "/share" + "\n");

    network_disable = input("Allow Acces Network connecton to the internet y,n? ");
    if(share_folder_daten == "y"):
        file1.write("network_disable = 1\n");
    if(share_folder_daten == "n"):
        file1.write("network_disable = 0\n");

    file1.close();
    create_Dockerfile(docker_container_name);
    return 0;




def create_a_docker_build(docker_container_name):
    os.system("mkdir -p " + "\"" + docker_container_name + "\"");
    os.system("cp " + buildfile  + " \""+ docker_container_name + "/build" + "\"");
    os.system("cp " + pulse_config  + " \""+ docker_container_name + "/pulse-client.conf" + "\"");

    os.system("chmod -R 777 \"" + docker_container_name + "\"");

    configure_build_file(docker_container_name);

    os.chdir(docker_container_name);
    build_start = input("Auto starting Container building y,n? ");
    if(build_start == "y"):
        os.system("./build" );
    else:
        print("Manuell docker building start");
        print("./build");
    os.chdir("..");
    create_system_links(docker_container_name);
    return 0;

def create_system_links(docker_container_name):
    os.chdir(docker_container_name);
    os.system("ln -sf build login");
    os.system("ln -sf build login_root");
    os.system("ln -sf build openra-ra");
    os.system("ln -sf build firefox");
    os.system("ln -sf build command");
    os.system("ln -sf build command_root");
    os.chdir("..");
    return 0;


def main():
    docker_container_name = input_name();
    if(os.path.isdir(docker_container_name) == True):
        print("Errror Name existirt schon");
        exit();
    create_a_docker_build(docker_container_name);
    os.chdir(docker_container_name);
    login_start = input("Auto login to Container y,n? ");
    if(login_start == "y"):
        os.system("./login");
    else:
        print("Manuell docker start des gebauten containers");
        print("./login");
    return 0;
main();



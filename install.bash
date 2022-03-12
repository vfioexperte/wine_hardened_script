#!/bin/bash
#3.0b
#ln -sf ../build build
chmod +x build
ln -sf build login_root 
ln -sf build login
ln -sf build run 
ln -sf build openra-ra 
ln -sf build firefox
ln -sf build command
ln -sf build command_root
ln -sf build edit_config
#ln -sf ../Code Code
cd archlinux_std_docker/archlinux_std_docker_big/archlinux_std_docker/
ln -sf ../../../build build
ln -sf ../../../Code Code
cp ../../../hidraw_acs_overrides_patch.py hidraw_acs_overrides_patch.py
ln -sf ../../../chmod_check.py chmod_check.py
cd archlinux_std_docker/
ln -sf build login
chmod +x build

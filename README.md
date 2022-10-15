this is a fork from https://github.com/kritzsie/steam-on-docker projeckt
	0.28q beta Wayland support and linux mint and linux ubuntu
	v0.31e_hotfix_56 lxc support archlinux and linuxmit and ubuntu

installation

archlinux pacman install command

	pacman -Syu  python-pip python cdemu-client cdemu-daemon vhba-module-dkms k3b lsscsi docker criu busybox mesa-demos mesa-utils archiso lxc lxc apparmor dnsmasq lxd archiso apparmor dnsmasq lxd
		
linux mint and ubuntu apt get install command

	apt-get install python3-pip lsscsi docker docker.io python3-pyqt5 mesa-utils lxc

linux add user groups for x11 or wayland user

	usermod -aG docker username
	usermod -aG optical username
	usermod -aG input username
	usermod -aG lxd username
	usermod -aG sudo username
	usermod -aG dbus username

first start
	systemctl enable docker
	systemctl start docker
	systemctl enable lxc
	systemctl start lxc
	systemctl start lxd
	lxd init
	systemctl restart lxd
	bash install.bash
	./manager
	./edit_config
	
for build a contienr

		cd archlinux_std_docker/archlinux_std_docker_big/archlinux_std_docker
		pacman_cache = /pacman_cache_foldeer...
		sudo mkdir -p /pacman_cache_foldeer
		chown -R username:users /pacman_cache_foldeer..
		#build must be run as root user
		bash install.bash
		su
		cd archlinux_std_docker/archlinux_std_docker_big/archlinux_std_docker
		./edit_config
		pacman_pakgage_install = pacman istall package
		sudo ./build		

		after build
		user from desktop start a terminal
		cd dockerfolder
		#archlinux
		./login
		#linux mint
		sudo ./login
		run app

archlinux:
auto run
singel comamnd

	#archlinux run user ls
	./command "ls"
	#archlinux root user ls
	./command_root "ls"
	
multi comamnd
args must be one not more
	./command "openra-ra \n bash"
	./command_root "openra-ra \n bash"

run config gui

	./edit_config

linux mint and ubuntu:
auto run
singel comamnd

	#archlinux run user ls
	sudo ./command "ls"
	#archlinux root user ls
	sudo ./command_root "ls"
	
multi comamnd
args must be one not more
	sudo ./command "openra-ra \n bash"
	sudo ./command_root "openra-ra \n bash"

run config gui

	sudo ./edit_config

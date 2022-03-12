this is a fork from https://github.com/kritzsie/steam-on-docker projeckt
	0.28q beta Wayland support and linux mint and linux ubuntu

	installation

		archlinux pacman install command
			pacman -Syu cdemu-client cdemu-daemon vhba-module-dkms k3b lsscsi docker criu busybox mesa-demos mesa-utils
		linux mint and ubuntu apt get install command
			apt-get install python3-pip lsscsi docker docker.io python3-pyqt5
		usermod -aG docker username
		usermod -aG optical username
		usermod -aG input username

		edit _config file
		pacman_cache = /pacman_cache_foldeer...
		sudo mkdir -p /pacman_cache_foldeer
		chown -R username:users /pacman_cache_foldeer..

		edit _config file

		bash install.bash
		#build must be run as root user
		bash install.bash
		su
		cd archlinux_std_docker/archlinux_std_docker_big/archlinux_std_docker
		edit _config file
		pacman_pakgage_install = pacman istall package
		./build		

		after build
		user from desktop start a terminal
		cd dockerfolder
		./login
		run app
	auto run
		singel comamnd
			#run user ls
			./command "ls"
			#run root user ls
			./command_root "ls"
		muti comamnd
			args must be one not more
			./command "openra-ra \n bash"
			./command_root "openra-ra \n bash"

	run config gui
		./edit_config

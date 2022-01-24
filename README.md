this is a fork from https://github.com/kritzsie/steam-on-docker projeckt
the application work onaly on archlinux.

	insatllation

		pacman -Syu cdemu-client cdemu-daemon vhba-module-dkms k3b lsscsi docker criu busybox mesa-demos mesa-utils
		usermod -aG docker username
		usermod -aG optical username
		usermod -aG input username

		edit _config file
		pacman_cache = /pacman_cache_foldeer...
		sudo mkdir -p /pacman_cache_foldeer
		chown -R username:users /pacman_cache_foldeer..

		edit _config file
		pacman_pakgage_install = pacman istall package

		bash install.bash
		#build must be run as root user
		./build

		after build

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

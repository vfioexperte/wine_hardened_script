this is a fork from https://github.com/kritzsie/steam-on-docker projeckt
the application work onaly on archlinux.

	insatllation

		pacman -Sy cdemu-client cdemu-daemon vhba-module-dkms k3b lsscsi docker
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
		./build

		after build

		./login
		run app
	auto run
		singel comamnd
			./command "ls" #run user ls
			./command_root "ls" #run user ls
		muti comamnd
			args must be one not more
			./command "cd  '/'&& ls" #run user ls
			./command_root "cd  / && ls" #run user ls

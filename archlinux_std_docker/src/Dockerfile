FROM archlinux

RUN echo "[multilib]" >>/etc/pacman.conf
RUN echo "Include = /etc/pacman.d/mirrorlist" >>/etc/pacman.conf
RUN pacman -Syu base base-devel --noconfirm -y
RUN useradd -m -g users -G video,audio,wheel empty

CMD empty

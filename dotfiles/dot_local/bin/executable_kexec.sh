# TODO: Make boot into same kernel as running. E.g. I'm on the LTS rn, I don't want to boot this.
sudo kexec -l /boot/vmlinuz-linux-zen --initrd=/boot/initramfs-linux-zen.img --reuse-cmdline
sudo systemctl kexec

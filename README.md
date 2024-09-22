# Jeep XJ Dash
here is the beginning project to do a different dash screen on my 1992 Jeep Cherokee XJ, some of the Gauges have to be reverse engineered a bit so this will take some time.

Disable X/Wayland sdl is fine do this as orangepi user:
sudo apt update
sudo apt upgrade
sudo reboot
sudo apt install python3-pygame-sdl2
sudo apt install python3-pygame
put the dash.py (and Symbola.ttf) file in /home/orangepi/dash.py
set it executable: chmod +x /home/orangepi/dash.py
Put systemd service file here: /etc/systemd/system/dash.service
sudo systemctl daemon-reload
sudo systemctl enable dash.service
sudo systemctl set-default multi-user.target
sudo reboot

Dashboard should show on boot now.

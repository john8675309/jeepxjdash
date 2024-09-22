# Jeep XJ Dash
here is the beginning project to do a different dash screen on my 1992 Jeep Cherokee XJ, some of the Gauges have to be reverse engineered a bit so this will take some time.

I am using an OrangePi Zero, an old Chromebook screen and a 30 pin HDMI LCD converter board:

https://www.amazon.com/dp/B06XC6SJF7

This Pi:

https://www.amazon.com/Orange-Pi-Zero-2W-Allwinner/dp/B0CHM7HN8P/


Disable X/Wayland sdl is fine do this as orangepi user:
```
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
```
Dashboard should show on boot now.

The board runs a little hot, and around 250% CPU all the time, so probably will do something where I don't redraw all the gauges unless there is a big change.

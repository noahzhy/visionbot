import os
import time
import glob
import sys


def run():
    for i in range(1, 31):
        f = open('ops//install_{0:04d}.sh'.format(i), 'w+')
        f.write('''
#!/bin/sh
cd /home/10moons/
echo "----------------auto install----------------"
sudo apt update
sudo apt upgrade -y
sudo apt -y install openssh-server
sudo apt -y install python3-dev
sudo apt -y install python3-pip
sudo apt -y install python3-opencv
sudo apt -y install nmap
sudo apt -y install python3-pandas
sudo apt -y install arp-scan
sudo apt -y install python3-tk
sudo apt -y install git
python3 -m pip install numpy==1.16.0
python3 -m pip install requests
# python3 -m pip install python3-nmap
python3 -m pip install python-nmap
wget -O tensorflow-1.10.1-cp36-cp36m-linux_aarch64.whl "http://192.168.5.147/tensorflow-1.10.1-cp36-cp36m-linux_aarch64.whl"
pip3 install tensorflow-1.10.1-cp36-cp36m-linux_aarch64.whl
echo "--------------install completed--------------"
cd /home/10moons/
sudo rm -rf *.whl
if [ -f "/etc/xdg/autostart/run.desktop" ]; then
  sudo rm -rf /etc/xdg/autostart/run.desktop
fi
echo "------------------autologin------------------"
sudo sh -c "echo [daemon] > /etc/gdm3/custom.conf"
sudo sh -c "echo AutomaticLoginEnable = true >> /etc/gdm3/custom.conf"
sudo sh -c "echo AutomaticLogin = 10moons >> /etc/gdm3/custom.conf"
echo "------------------autostart------------------"
sudo sh -c "echo 'cd /home/10moons/visionbot/ && python3 run.py' > /home/10moons/run.sh"
sudo chmod +x /home/10moons/run.sh
if [ ! -d "/home/10moons/.config/autostart/" ]; then
  mkdir /home/10moons/.config/autostart/
fi
cd /home/10moons/.config/autostart
sudo sh -c "echo '[Desktop Entry]\nName=auto_run\nType=Application\nExec=bash /home/10moons/run.sh' > /home/10moons/.config/autostart/run.desktop"
echo "-----------------update code-----------------"
cd /home/10moons/
if [ -d "/home/10moons/FD-Nano/" ]; then
  sudo rm -rf /home/10moons/FD-Nano/
fi
if [ -d "/home/10moons/visionbot/" ]; then
  sudo rm -rf /home/10moons/visionbot/
fi
sudo -u 10moons git clone https://github.com/noahzhy/visionbot.git
cd /home/10moons/visionbot/
sudo mv fall_0001.txt fall_{0:04d}.txt
echo "-----------------all finish------------------"
        '''.format(i))


if __name__ == "__main__":
    run()
  
# wget -qO- http://222.109.16.122/install_0001.sh | sudo sh
# wget -qO- http://visiongo.ai/ops/install_0030.sh | sudo sh

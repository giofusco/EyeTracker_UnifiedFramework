
USB port for IMU sensor
from terminal launch dmesg, look for cp210x converter now attached to... (something like ttyUSB0)

User has to be in dialout group
sudo usermod -a -G dialout $USER

Python dependencies
pyserial : sudo pip install pyserial


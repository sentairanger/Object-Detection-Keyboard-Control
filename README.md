# Object-Detection-Keyboard-Control

## Overview of the Project

This is based on the project I did previously but with keyboard control now. If you want to see my other project click [here.](https://github.com/sentairanger/Torvalds-Computer-Vision). Here the robot moves using key commands and can be used to detect objects while in movement. 

### Getting Things Started

To begin here are the things I have used for the project. However, you can swap things out as needed:

* Robot Chassis. I used DFRobot's Devastator Tank Mobile Platform for this project. You can use any chassis you want.
* Pi Camera. Use any Pi Camera you wish.
* Raspberry Pi 3B+. You don't need to use this one but since OpenVINO is required for this project you'll need a decent board. You can use the 3B or even the 3A+. The 4B requires more power and will require adequate cooling. 
* Intel NCS2.
* 5V 3A USB power bank. A UBEC can be used but beware of the risks.
* 6 AA Batteries. Rechargable NiMi batteries can be used instead. 
* CamJam Edukit 3 Motor Controller. You can swap this out for any other controller but adjust the code accordingly.
* Two HDD LEDs. These aren't required but if you want to give your robot eyes you should consider them. You can also use LEDs you have lying around, resistors, dupont wires and bezels to make your own eyes.
* Heatsinks. Only required if you want proper cooling.
* Micro SD card with Raspbian Buster installed. 
* Keyboard and mouse for initial setup

### Required software

Here's the software that was needed for me to run the robot. You can also swap out some of these at your discretion:

* Raspbian Buster. You can download [here.](https://www.raspberrypi.org/downloads/raspbian/)
* Intel OpenVINO. Download the software from [here.](https://download.01.org/opencv/2020/openvinotoolkit/2020.1/)
* Installed prerequisites. Follow this tutorial [here.](https://www.pyimagesearch.com/2019/04/08/openvino-opencv-and-movidius-ncs-on-the-raspberry-pi/)
* Clone this repository.
* Enable RealVNC on the Pi as you want to run this headlessly. 
* VNC Viewer to view the Pi on another machine. Download [here.](https://www.realvnc.com/en/connect/download/viewer/)

### Required Steps

Here are the steps you need to take to run the robot:

* Assemble the robot.
* Make sure you downloaded Raspbian and installed it on your Micro SD card.
* Insert the Micro SD card on your robot. 
* Make sure you follow the tutorial I linked about to install all the prerequisites and openVINO. Also, make sure to install a virtual environment by typing `sudo pip install virtualenv`.
* Once you installed openVINO run the `source /opt/intel/openvino/bin/setupvars.sh` to source the environment. To activate the python environment first run `virtualenv -p python3 venv` to create a python3 environment called venv. You can call your environment whatever you want.
* Clone the repository and make sure you `cd` into the repository you downloaded.
* Next, enable RealVNC by going into Menu > Preferences > Raspberry Pi Configuration > Interfaces > VNC > Enable
* Enable the Pi Camera by going into Menu > Preferences > Raspberry Pi Configuration > Interfaces > Camera > Enable 
* Check your ip address by typing `ifconfig`. Once you know what your address is unplug the HDMI and go to the machine where you installed VNC Viewer.
* On VNC Viewer, go to File > New Connection. On VNC server type the address or your hostname. In this case, your hostname would be pi by default. Once you set that up click on your new connection and you should be presented with the Pi desktop.
* Enable the camera on VNC Viewer by going into Menu > Options > Troubleshooting > Enable experimental direct capture mode
* Once everything is setup, run the code by typing `python object_detection_keyboard_robot.py --model MobileNetSSD_deploy.caffemodel --prototxt MobileNetSSD_deploy.prototxt`.
* The follwing arguments are required:
* `--model`: This chooses which model to run
* `--prototxt`: This chooses which prototxt to use
* Once it runs you can type WASD to see the robot move and you can see what objects are being detected by the robot.

### 2024 Update

This project like my Object Detection Robot application will work with 32 bit Pi OS Bullseye thanks to this [issue](https://github.com/openvinotoolkit/openvino/issues/8789). However this project will cease to work after 2024 due to Intel dropping support for the NCS2.

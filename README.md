# TeslaModel3HUD
Head-Up Display for the Tesla Model 3 using a Raspberry Pi and CAN data captured from the car.

## Features
This HUD displays similar information to what is shown on the top left of the Tesla Model 3's display. 

* Current date and time, converted from UTC to local time at the beginning of the drive
* Current speed when driving, "P" when parked, "H" when brake hold is active
* Turn signal state (may not blink exactly like the car display though)
* Current "gear" state (i.e. P/R/N/D)
* Current state-of-charge in percentage 

To-do wishlist (not sure if these are all possible using CAN data):
* Next navigation step
* Reduce display brightness when the car display switches to night mode
* Current TACC speed if cruise is enabled

## Hardware
* [Raspberry Pi 3B+](https://smile.amazon.com/gp/product/B07BDR5PDW/) or [Nvidia Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/): performance is better with Jetson Nano
* Sunlight-readable display, e.g. [Newhaven Display NHD-7.0-HDMI-N-RSXN-CTU](http://www.newhavendisplay.com/nhd70hdminrsxnctu-p-9552.html)
* CAN harness for the Tesla Model 3, I am using [this one](http://store.evtv.me/proddetail.php?prod=TeslaModel3CANKit)
* [Beamsplitter mirror](https://telepromptermirror.com/glass-teleprompter-mirror/), 87mm x 157mm, thickness 1/8", transparency 30R/70T, rounded corners
* [3D printed mounts](https://www.thingiverse.com/thing:3496105) to place your monitor and mirror in the right place for driver's line-of-sight in the car
* [Car 12V power splitter](https://smile.amazon.com/gp/product/B07CM7PJQB/) to power the Pi and the monitor, while leaving a 12V socket open for other devices
* [HDMI cable](https://smile.amazon.com/gp/product/B01JO9T43G/) at least 6 feet long
* [Car power cable for the monitor](https://smile.amazon.com/gp/product/B07BSFSW8N/)
* [5V, 2A car power cable](https://smile.amazon.com/gp/product/B075XMTQJC/) for the Pi with a switch

## Software
* [Raspbian Stretch Lite](https://downloads.raspberrypi.org/raspbian_lite_latest)
* [unclutter](https://wiki.archlinux.org/index.php/unclutter)
* [PyGObject](https://pygobject.readthedocs.io/en/latest/index.html)

## Instructions

** To be updated **
Get a Raspberry Pi 3B+ with Raspbian Lite

sudo apt install git python3-pip unclutter
pip3 install pyserial

## Pictures

HUD in action
![HUD in action](https://i.imgur.com/tpscMLz.jpg)

Close-up of driver's view of HUD
![Close-up of driver's view of HUD](https://i.imgur.com/9UdMikN.jpg)

Side view of monitor and mirror mounts
![Side view of mounts](https://thingiverse-production-new.s3.amazonaws.com/assets/ca/d1/42/7c/10/IMG_20190316_120601.jpg)

Close front view of HUD
![Close front view of HUD](https://thingiverse-production-new.s3.amazonaws.com/assets/f6/e7/c7/c6/02/IMG_20190316_121405.jpg)

## Thanks
This project owes a lot to the following people who helped me:
* [JWardell](https://teslaownersonline.com/members/jwardell.1513/) at the Tesla Owners Online forums
* [Collin80](https://github.com/collin80) here at Github

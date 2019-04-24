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

The Jetson Nano is more expensive, but it can handle 5-10 times higher screen refres rates than the RPi. This can make for a nicer experience with the speed updating real-time when accelerating, or the turn signal indicators blinking in alignment with the car display. Please note that the Jetson Nano does not have onboard Wi-Fi, so you will need to pull it out of the car for troubleshooting or changes. If you want Wi-Fi on the Jetson Nano, you will need a [USB adapter like this one](https://smile.amazon.com/gp/product/B003MTTJOY/). 

## Software
* [Raspbian Stretch Desktop](https://downloads.raspberrypi.org/raspbian_latest) if using a Raspberry Pi
* [Linux4Tegra](http://developer.nvidia.com/embedded/dlc/jetson-nano-dev-kit-sd-card-image) if using a Jetson Nano
* [unclutter](https://wiki.archlinux.org/index.php/unclutter)
* [PyGObject](https://pygobject.readthedocs.io/en/latest/index.html)

## Instructions

Connect up the Pi or Nano with your LCD monitor and a USB keyboard. 

Get the Raspberry Pi 3B+ loaded with Raspbian Desktop, or the Jetson Nano with the initial image of L4T. You can remove packages like LibreOffice and Mathematica as we don't need them.

If you use the Jetson Nano, switch to the GNOME Desktop (instead of the default Unity Desktop that L4T comes with). You can do this by clicking on the settings icon at the login screen. In the Jetson Nano, you also need to auto-hide the Dock and install the GNOME extension "Hide Top Bar". 

Install the needed software:
* `sudo apt install git python3-pip unclutter`
* `pip3 install pyserial`
* Download 'Gotham Book' font and put the TTF file in `.fonts` in your home directory

Clone this project and get it running:
* `git clone https://github.com/ppamidimarri/TeslaModel3HUD`
* `chmod +x serial_test.py reader_test.py tm3hud.py gui_test.py`

Connect the CAN harness to the USB port and check that `/dev/ttyUSB0` is now available. If your CAN device shows up with a different path than `/dev/ttyUSB0`, you need to update `serial_test.py` and `canreader.py` with that path. On the Jetson Nano, you need to add your account to the group `dialout` if you want to run the HUD application without `sudo`. 

Open a terminal and try to run `serial_test.py`. You should see a bunch of CAN messages. Then try to run `reader_test.py`, you should see summary results like speed, state-of-charge, etc. 

If both these tests run OK, check the path to `hud.glade` inside the `tm3hud.py` and `gui_test.py` files and update them if needed. You can now test the GUI with `tm3hud.py`. It should run in full-screen mode. If you want to test just the GUI layout without real data from the CAN harness, you can run `gui_test.py`. This is useful when your Pi or Nano is not connected to the CAN harness in the car. 

If your GUI is starting in full-screen mode, it is time to set the HUD to start up on boot. The steps are different for each device.

**Raspberry Pi**

We have to edit two configuration files.

`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`, remove the `@xscreensaver` line, and add:
```
@xset s off
@xset -dpms
@xset s noblank
@/home/pi/TeslaModel3HUD/tm3hud.py
```

`sudo nano /boot/config,txt`, and at the end, add:
```
display_rotate=0x10000
```

If you are using a Pi, reduce the screen refresh rate by looking in `tm3hud.py` for the line that contains `GObject.timeout_add` and increase the number. This is what works best for me in my testing:
```
GObject.timeout_add(500, self.update_data)
```

**Jetson Nano**

Disable the screensaver and screen off options. 

Under Activities, search for Startup activities. Add two new startup activities:
* `xrandr -x` to reflect the display
* Full path to tm3hud.py, to start the HUD GUI

Now restart your device with `sudo reboot` and the GUI should start up! 

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

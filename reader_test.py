#!/usr/bin/env python3

import canreader
import time
import threading

reader = canreader.CANReader()

try:
	for i in range(1, 300):
		print("Speed: {0}, State: {5}, Gear: {1}, Hold: {2}, SOC: {3:.1f}, Capacity: {8:.1f}, Latitude: {6}, Longitude: {7}, Stamp: {4}".format(
			reader.get_speed(),
			reader.get_gear(),
			reader.get_brake_hold(),
			reader.get_soc(),
			reader.get_timestamp(),
			reader.get_drive_state(),
			reader.get_latitude(),
			reader.get_longitude(),
			reader.get_battery_capacity()
		))
		time.sleep(1)
except KeyboardInterrupt:
	reader.close()

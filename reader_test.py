#!/usr/bin/env python3

import canreader
import time
import threading

reader = canreader.CANReader()

try:
	for i in range(1, 300):
		print("State: {5}, Gear: {1}, Hold: {2}, Speed: {0}, SOC: {3:.1f}, Capacity: {8:.1f}, Stamp: {4}".format(
			reader.get_speed(),
			reader.get_gear(),
			reader.get_brake_hold(),
			reader.get_soc(),
			reader.get_timestamp(),
			reader.get_drive_state(),
			reader.get_battery_capacity()
		))
		time.sleep(1)
except KeyboardInterrupt:
	reader.close()

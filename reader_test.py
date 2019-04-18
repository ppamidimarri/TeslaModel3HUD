#!/usr/bin/env python3

import canreader
import time
import threading

reader = canreader.CANReader(log_level=3)

try:
	for i in range(1, 300):
		print("State: {5}, Gear: {1}, Hold: {2}, Speed: {0}, SOC: {3:.1f}%, Capacity: {6:.1f}%, Left Turn: {7}, Right Turn: {8}, Stamp: {4}".format(
			reader.get_speed(),
			reader.get_gear(),
			reader.get_brake_hold(),
			reader.get_soc(),
			reader.get_timestamp(),
			reader.get_drive_state(),
			reader.get_battery_capacity(),
			reader.get_turn_left_on(),
			reader.get_turn_right_on()
		))
		time.sleep(1)
except KeyboardInterrupt:
	reader.close()

#!/usr/bin/env python3

import serial

ser = serial.Serial(port="/dev/ttyUSB0", baudrate=1000000)
sep = b'\xf1\x00'
speed = None

while True:
	line = ser.readline()

	parts = line.partition(sep)
	while True:
		frame = parts[0]
		mlen = len(frame)
		if mlen > 8:
			frame_id = frame[4] + 256 * (frame[5] + 256 * (frame[6] + 256 * frame[7]))
			print("{0:03x}: {1}".format(frame_id, frame[9:].hex()))
		else:
			print("Length: {0}, Frame: {1}".format(mlen, frame.hex()))
		parts = parts[2].partition(sep)
		if len(parts[2]) <= 0:
			break;

import serial, threading, datetime

LOG_LEVEL = 0 # 1=errors, 2=info, 3=debug

class CANReader:
	def __init__(self, port="/dev/ttyUSB0", baudrate=1000000, log_level=None):
		self.ser = serial.Serial(port, baudrate)
		self.sep = b'\xf1\x00'
		self.speed = 0
		self.gear = 2
		self.drive_state = 0
		self.brake_hold = 0
		self.soc = 0
		self.timestamp = datetime.datetime.utcnow()
		self.battery_capacity = 0
		self.turn_left_on = 0
		self.turn_right_on = 0

		if log_level is None:
			self.log_level = LOG_LEVEL
		else:
			self.log_level = log_level

		self.read_thread = threading.Thread(target=self.read, args=())
		self.stop_reading = False
		self.read_thread.daemon = True
		self.read_thread.start()

	def log(self, level, text):
		if level <= self.log_level:
			print(text)

	def close(self):
		self.stop_reading = True
		self.ser.flush()
		self.ser.close()

	# Read CAN messages, this runs in a background thread

	def read(self):
		while not self.stop_reading:
			line = self.ser.readline()

			parts = line.partition(self.sep)
			while True:
				frame = parts[0]
				mlen = len(frame)
				if mlen > 8:
					frame_id = frame[4] + 256 * (frame[5] + 256 * (frame[6] + 256 * frame[7]))
					if frame_id == 0x257 and mlen > 12: 	# UI speed
						self.speed = frame[12]
					elif frame_id == 0x118 and mlen > 12: 	# Gear and Brake Hold status
						self.process_drive_state_signal(frame[11], frame[12])
					elif frame_id == 0x318 and mlen > 14: 	# UTC Timestamp
						self.process_timestamp_signal(frame[9:])
					elif frame_id == 0x292 and mlen > 10: 	# State of Charge
						self.soc = self.process_soc_signal(frame[9], frame[10])
					elif frame_id == 0x352 and mlen > 15: 	# Battery Capacity
						self.process_battery_capacity_signal(frame[9:])
					elif frame_id == 0x3F1 and mlen > 15:	# Turn signals
						self.process_turn_signal(frame[15])
					else:
#						self.log(2, "Unknown Frame ID: {0:03x}, {1}".format(frame_id, self.format_frame(frame[9:])))
						pass
				else:
#					self.log(1, "Bad Length: {0}, {1}".format(mlen, self.format_frame(frame)))
					pass
				parts = parts[2].partition(self.sep)
				if len(parts[2]) <= 0:
					break

	# Process various CAN messages to extract relevant data

	def process_turn_signal(self, byte):
		binary = "{0:08b}".format(byte)
		self.turn_left_on = int(binary[5], 2)
		self.turn_right_on = int(binary[3], 2)

	def process_battery_capacity_signal(self, bytes):
		signal = ""
		for b in reversed(bytes):
			signal += "{0:08b}".format(b)
		full = int(signal[-10:], 2)/10
		remaining = int(signal[-20:-10], 2)/10
		expected = int(signal[-30:-20], 2)/10
		ideal = int(signal[-40:-30], 2)/10
		buffer = int(signal[-58:-50], 2)/10
		if full != 0:
			self.battery_capacity = 100*(remaining-buffer)/(full-buffer)

	def process_timestamp_signal(self, bytes):
		year = bytes[0] + 2000
		month = bytes[1]
		second = bytes[2]
		hour = bytes[3]
		day = bytes[4]
		minute = bytes[5]
		if self.is_valid_date(year, month, day, hour, minute, second):
			self.timestamp = datetime.datetime(year, month, day, hour, minute, second)
		else:
			self.log(1, "Bad date, yr: {0}, mon: {1}, day: {2}, hr: {3}, min: {4}, sec: {5}, {6}".format(
				year, month, day, hour, minute, second, self.format_frame(bytes)))

	def process_soc_signal(self, byte1, byte2):
		binary1 = "{0:08b}".format(byte1)
		binary2 = "{0:08b}".format(byte2)
		value = binary2[6:] + binary1
		return int(value, 2)/10

	def process_drive_state_signal(self, byte1, byte2):
		binary1 = "{0:08b}".format(byte1)
		binary2 = "{0:08b}".format(byte2)
		self.gear = int(binary1[1:4], 2)
		self.drive_state = int(binary1[5:], 2)
		self.brake_hold = int(binary2[5], 2)

	# Utilities for processing data

	def format_frame(self, frame):
		buf = "Frame Hex: "
		for b in frame:
			buf += "{0}-".format(hex(b))
		buf = buf[:-1]
		buf += " Frame Dec: "
		for b in frame:
			buf += "{0}-".format(b)
		return buf[:-1]

	def is_valid_date(self, year, month, day, hour, minute, second):
		if year < 2000 or year > 2100:
			return False
		elif month < 1 or month > 12:
			return False
		elif day < 1 or day > 31:
			return False
		elif hour < 0 or hour > 23:
			return False
		elif minute < 0 or minute > 59:
			return False
		elif second < 0 or second > 59:
			return False
		else:
			return True

	# Make data available for display

	def get_speed(self):
		return self.speed

	def get_gear(self):
		gear_map = {
			0: "D",
			2: "P",
			4: "R",
			6: "N"
		}
		return gear_map.get(self.gear, "-")

	def get_drive_state(self):
		drive_state_map = {
			0: "Idle",
			1: "Charge",
			2: "Park",
			5: "Drive"
		}
		return drive_state_map.get(self.drive_state, "-")

	def get_brake_hold(self):
		return self.brake_hold

	def get_soc(self):
		return self.soc

	def get_timestamp(self):
		return self.timestamp

	def get_battery_capacity(self):
		return self.battery_capacity

	def get_turn_left_on(self):
		return self.turn_left_on

	def get_turn_right_on(self):
		return self.turn_right_on

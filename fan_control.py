#!/usr/bin/env python3

import subprocess, threading, time

class FanController:
	def __init__(self,
			temperature_device = "/sys/devices/virtual/thermal/thermal_zone0/temp",
			fan_device = "/sys/devices/pwm-fan/target_pwm"):
		self.temperature_filename = temperature_device
		self.fan_filename = fan_device

		self.iterate_thread = threading.Thread(target=self.iterate, args=())
		self.stop_iterating = False

		subprocess.call("/usr/bin/jetson_clocks")

	def get_temperature(self):
		file = open(self.temperature_filename, "r")
		temperature = int(file.readline(), 10)/1000
		file.close()
		return temperature

	def turn_fan_on(self):
		subprocess.call('echo 255 > {0}'.format(self.fan_filename), shell=True)
		return True

	def turn_fan_off(self):
		subprocess.call('echo 255 > {0}'.format(self.fan_filename), shell=True)
		return True

	def start_iterating(self):
		self.iterate_thread.start()

	def send_stop(self):
		self.stop_iterating = True

	def iterate(self):
		while not self.stop_iterating:
			if self.get_temperature() > 50:
				self.turn_fan_on()
			else:
				self.turn_fan_off()
			time.sleep(600)

controller = FanController()
controller.start_iterating()

#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk
from datetime import datetime
import subprocess
import canreader

class HeadUpDisplay(Gtk.Window):
	def __init__(self):
		self.font_face = 'Gotham'
		self.speed_markup = "<span font='120' face='" + self.font_face + "' color='{0}' font_features='tnum=1,lnum=1'>{1}</span>"
		self.unit_markup = "<span font='20' face='" + self.font_face + "' color='{0}'><b>{1}</b></span>"
		self.gear_active_markup = "<span font='20' face='" + self.font_face + "' color='{0}'><b>{1}</b></span>"
		self.gear_inactive_markup = "<span font='20' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.hold_markup = "<span font='20' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.time_markup = "<span font='20' face='" + self.font_face + "' color='{0}'><b>{1}</b></span>"
		self.date_markup = "<span font='20' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.soc_markup = "<span font='20' face='" + self.font_face + "' color='{0}'>{1:.0f}%</span>"
		self.time_format = "%-I:%M %p"
		self.date_format = "%a, %b %-d"
		self.utc_offset = datetime.utcnow() - datetime.now()

		self.reader = canreader.CANReader()

		settings = Gtk.Settings.get_default()
		settings.set_property("gtk-theme-name", "Adwaita-dark")

		self.builder = Gtk.Builder()
		self.builder.add_from_file("/home/pi/hud/hud.glade")
		self.builder.get_object("mainPanel").override_background_color(
			Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0,1))
		self.builder.get_object("mainPanel").connect("destroy", self.on_destroy)

		self.builder.get_object("P").set_markup(self.gear_active_markup.format(self.get_active_text_color(), "P"))
		self.builder.get_object("R").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "R"))
		self.builder.get_object("N").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "N"))
		self.builder.get_object("D").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "D"))
		self.builder.get_object("Blank 1").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))
		self.builder.get_object("Blank 2").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))
		self.builder.get_object("Blank 3").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))

		self.update_data()
		self.update_system_date()

	def update_data(self):
		speed = self.reader.get_speed()
		gear = self.reader.get_gear()
		hold = self.reader.get_brake_hold()
		soc = self.reader.get_battery_capacity()
		stamp = self.get_local_timestamp()

		self.builder.get_object("SOC").set_markup(self.soc_markup.format(self.get_text_color(), soc))
		self.builder.get_object("Time").set_markup(
			self.time_markup.format(self.get_text_color(), stamp.strftime(self.time_format).upper()))
		self.builder.get_object("Date").set_markup(
			self.hold_markup.format(self.get_text_color(), stamp.strftime(self.date_format)))

		self.update_speed(speed, hold, gear)
		self.update_gear(self.reader.get_gear())

		return True

	def update_speed(self, speed, hold, gear):
		if gear == "P":
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), "P"))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), ""))
		elif hold and speed == 0:
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), "H"))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), ""))
		else:
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), speed))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), "MPH"))
		return True

	def update_gear(self, gear):
		if gear == "P":
			self.builder.get_object("P").set_markup(self.gear_active_markup.format(self.get_active_text_color(), "P"))
			self.builder.get_object("R").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "R"))
			self.builder.get_object("N").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "N"))
			self.builder.get_object("D").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "D"))
		elif gear == "R":
			self.builder.get_object("P").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "P"))
			self.builder.get_object("R").set_markup(self.gear_active_markup.format(self.get_active_text_color(), "R"))
			self.builder.get_object("N").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "N"))
			self.builder.get_object("D").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "D"))
		elif gear == "N":
			self.builder.get_object("P").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "P"))
			self.builder.get_object("R").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "R"))
			self.builder.get_object("N").set_markup(self.gear_active_markup.format(self.get_active_text_color(), "N"))
			self.builder.get_object("D").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "D"))
		elif gear == "D":
			self.builder.get_object("P").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "P"))
			self.builder.get_object("R").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "R"))
			self.builder.get_object("N").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "N"))
			self.builder.get_object("D").set_markup(self.gear_active_markup.format(self.get_active_text_color(), "D"))
		return True

	def update_system_date(self):
		stamp = self.reader.get_timestamp()
		ret_val = subprocess.call('sudo date -u --set="{0}"'.format(stamp.strftime("%Y%m%d %H:%M:%S")), shell=True)

	def get_text_color(self):
		return self.get_active_text_color()

	def get_passive_text_color(self):
		return "#666666"

	def get_inactive_text_color(self):
		return "#888888"

	def get_active_text_color(self):
		return "#FFFFFF"

	def start_updater(self):
		GObject.timeout_add(500, self.update_data)

	def get_local_timestamp(self):
		return self.reader.get_timestamp() - self.utc_offset

	def on_destroy(self, widget, data=None):
		self.reader.close()
		Gtk.main_quit()

hud = HeadUpDisplay()
window = hud.builder.get_object("mainPanel")
window.fullscreen()
window.show_all()
hud.start_updater()

Gtk.main()

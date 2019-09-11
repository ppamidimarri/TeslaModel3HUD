#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk
from datetime import datetime
import random

class HeadUpDisplay(Gtk.Window):
	def __init__(self):
		self.font_face = 'Gotham'
		self.speed_font_size = '120'
		self.turn_font_size = '60'
		self.other_font_size = '18'
		self.speed_markup = "<span font='" + self.speed_font_size + "' face='" + self.font_face + "' color='{0}' font_features='tnum=1,lnum=1'>{1}</span>"
		self.unit_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'><b>{1}</b></span>"
		self.gear_active_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'><b>{1}</b></span>"
		self.gear_inactive_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.hold_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.time_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'><b>{1}</b></span>"
		self.date_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.soc_markup = "<span font='" + self.other_font_size + "' face='" + self.font_face + "' color='{0}'>{1:.0f}%</span>"
		self.turn_markup = "<span font='" + self.turn_font_size + "' face='" + self.font_face + "' color='{0}'>{1}</span>"
		self.time_format = "%-I:%M %p"
		self.date_format = "%a, %b %-d"
		self.utc_offset = datetime.utcnow() - datetime.now()
		self.current_speed = 0
		self.gear_values = ["P", "R", "N", "D"]

		settings = Gtk.Settings.get_default()
		settings.set_property("gtk-theme-name", "Adwaita-dark")

		self.builder = Gtk.Builder()
		self.builder.add_from_file("/home/pavan/TeslaModel3HUD/hud.glade")
		self.builder.get_object("mainPanel").override_background_color(
			Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0,1))
		self.builder.get_object("mainPanel").connect("destroy", self.on_destroy)

		self.builder.get_object("P").set_markup(self.gear_active_markup.format(self.get_active_text_color(), "P"))
		self.builder.get_object("R").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "R"))
		self.builder.get_object("N").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "N"))
		self.builder.get_object("D").set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), "D"))
		self.builder.get_object("Blank Top").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))
		self.builder.get_object("Blank Gear 1").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))
		self.builder.get_object("Blank Gear 2").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))
		self.builder.get_object("Blank Gear 3").set_markup(self.hold_markup.format(self.get_inactive_text_color(), ""))

		self.update_data()

	def update_data(self):
		speed = random.randint(0, 75)
		gear = self.gear_values[random.randint(0, 3)]
		hold = random.randint(0, 2)
		states = ["Idle", "Park", "Charge", "Drive"]
		state = states[random.randint(0, 3)]
		soc = random.randint(0, 100)
		stamp = self.get_local_timestamp()

		self.builder.get_object("SOC").set_markup(self.soc_markup.format(self.get_text_color(), soc))
		self.builder.get_object("Time").set_markup(
			self.time_markup.format(self.get_text_color(), stamp.strftime(self.time_format).upper()))
		self.builder.get_object("Date").set_markup(
			self.date_markup.format(self.get_text_color(), stamp.strftime(self.date_format)))

		if abs(self.current_speed - speed) < 20:
			self.update_speed(speed, hold, gear, state)
			self.update_gear(gear, state)
		self.update_turns(random.randint(0, 2), random.randint(0, 2))

		return True

	def update_turns(self, left, right):
		if left:
			self.builder.get_object("LeftTurn").set_markup(self.turn_markup.format(self.get_turn_color(), "\u25c0"))
		else:
			self.builder.get_object("LeftTurn").set_markup(self.turn_markup.format(self.get_text_color(), ""))

		if right:
			self.builder.get_object("RightTurn").set_markup(self.turn_markup.format(self.get_turn_color(), "\u25b6"))
		else:
			self.builder.get_object("RightTurn").set_markup(self.turn_markup.format(self.get_text_color(), ""))

		return True

	def update_speed(self, speed, hold, gear, state):
		if state == "Park" or state == "Idle" or gear == "P":
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), "P"))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), ""))
		elif state == "Charge":
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), "C"))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), "PLUGGED IN"))
		elif hold and speed == 0:
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), "H"))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), "HOLD"))
		else:
			self.builder.get_object("Speed").set_markup(self.speed_markup.format(self.get_text_color(), speed))
			self.builder.get_object("SpeedUnit").set_markup(self.unit_markup.format(self.get_passive_text_color(), "MPH"))
			self.current_speed = speed
		return True

	def update_gear(self, gear, state):
		if state == "Drive":
			self.set_gear_value(gear)
		else:
			self.set_gear_value("P")
		return True

	def set_gear_value(self, value):
		for item in self.gear_values:
			if value == item:
				self.builder.get_object(item).set_markup(self.gear_active_markup.format(self.get_active_text_color(), item))
			else:
				self.builder.get_object(item).set_markup(self.gear_inactive_markup.format(self.get_inactive_text_color(), item))
		return True

	def get_text_color(self):
		return self.get_active_text_color()

	def get_passive_text_color(self):
		return "#555555"

	def get_inactive_text_color(self):
		return "#666666"

	def get_active_text_color(self):
		return "#FFFFFF"

	def get_turn_color(self):
		return "#44FF44"

	def start_updater(self):
		GObject.timeout_add(100, self.update_data)

	def get_local_timestamp(self):
		return datetime.utcnow() - self.utc_offset

	def on_destroy(self, widget, data=None):
		Gtk.main_quit()

hud = HeadUpDisplay()
window = hud.builder.get_object("mainPanel")
window.fullscreen()
window.resize(800, 480)
window.set_position(Gtk.WindowPosition.CENTER)
hud.start_updater()
window.show_all()

Gtk.main()

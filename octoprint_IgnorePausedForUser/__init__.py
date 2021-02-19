# coding=utf-8

import octoprint.plugin
from octoprint.events import eventManager, Events
import re
import logging, logging.handlers
import os
from .history import History

class IgnorePausedForUser(octoprint.plugin.StartupPlugin,
						  octoprint.plugin.EventHandlerPlugin,
						  octoprint.plugin.AssetPlugin,						  
						  octoprint.plugin.TemplatePlugin,
                		  octoprint.plugin.SettingsPlugin):

	## checkPausedForUser		
	def checkPausedForUser(self, comm, line, *args, **kwargs):
		if "echo:busy: paused for user" in line:
			if self._settings.get(["enabled"]):
				self._printer.commands("M108", force=True)
				self.count += 1
				messageString = "Sent M108 to resume after 'Paused for user'\nPauses received during this print: <strong>%s</strong>" % self.count
				self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=messageString, hide=self._settings.get(["autoclose"])))
				self.history.UpdateCount(self.count)
				self.logger.debug("GCODE received: '%s'" % line)
				self.logger.info("Sent M108")
		return line
		
	## printStarted
	def printStarted(self, payload):
		self.logger.debug("IgnorePausedForUser - PRINT STARTED")
		self.count = 0
		self.history.StartJob(payload)		

	## printStopped
	def printStopped(self, payload, cancelled):
		if cancelled:
			self.logger.debug("IgnorePausedForUser - PRINT CANCELLED")
		else:
			self.logger.debug("IgnorePausedForUser - PRINT DONE")
		self.history.StopJob(cancelled)


	## on_after_startup
	def on_after_startup(self):
		# count
		self.count = 0
		# history
		self.history = History(self._settings.get_plugin_data_folder())
		# logger
		logFile = self._settings.get_plugin_logfile_path()[1:]
		formatter = logging.Formatter("%(asctime)s - %(levelname)s > %(message)s")
		self.logger = logging.getLogger("IgnorePausedForUserPlugin")
		self.logger.setLevel(logging.DEBUG)
		handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=1000000, backupCount=3)
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		# startup
		enabled = self._settings.get(["enabled"])
		autoclose = self._settings.get(["autoclose"])
		self.logger.debug("IgnorePausedForUser - STARTUP")
		self.logger.info(f"Enabled: '{enabled}' Autoclose: '{autoclose}'")

	## on_event
	def on_event(self, event, payload):
		if event == Events.PRINT_STARTED:
			self.printStarted(payload)
		elif event == Events.PRINT_DONE:
			self.printStopped(payload, False)
		elif event == Events.PRINT_FAILED:
			self.printStopped(payload, True)

	##-- AssetPlugin hooks
	def get_assets(self):
		return dict(js=["js/IgnorePausedForUser.js"])
		
	##-- Settings hooks
	def get_settings_defaults(self):
		return dict(enabled=False, autoclose=True)	
	
	##-- Template hooks
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]

	##-- Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			IgnorePausedForUser=dict(
				displayName="IgnorePausedForUser",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="DavideM84",
				repo="OctoPrint-IgnorePausedForUser",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/DavideM84/OctoPrint-IgnorePausedForUser/archive/v{version}.zip"
			)
		)

__plugin_name__ = "IgnorePausedForUser"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = IgnorePausedForUser()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.checkPausedForUser,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


# coding=utf-8

import octoprint.plugin
from octoprint.events import eventManager, Events
import re
import logging, logging.handlers
import os
from .history import History
from flask import jsonify, Flask

class IgnorePausedForUser(octoprint.plugin.StartupPlugin,
						  octoprint.plugin.EventHandlerPlugin,
						  octoprint.plugin.AssetPlugin,						  
						  octoprint.plugin.TemplatePlugin,
                		  octoprint.plugin.SettingsPlugin,
						  octoprint.plugin.BlueprintPlugin):

	## checkPausedForUser		
	def checkPausedForUser(self, comm, line, *args, **kwargs):
		if self.isEnabled():
			if "echo:busy: paused for user" in line:
				# send M108 to printer for continue
				self._printer.commands("M108", force=True)
				# increase counter
				self.count += 1
				# message to user
				messageString = "Sent M108 to resume after 'Paused for user'\nPauses received during this print: <strong>%s</strong>" % self.count
				self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=messageString, hide=self._settings.get(["autoclose"])))
				# info
				self.logger.info(f"GCODE received: '{line.strip()}'")
				self.logger.info("GCODE Sent M108")
				## update history
				self.history.UpdateCount(self.count)
		return line
		
	## printStarted
	def printStarted(self, payload):
		self.logger.info("New print STARTED")
		self.count = 0
		self.history.StartJob(payload)		

	## printStopped
	def printStopped(self, payload, cancelled):
		str = "CANCELLED" if cancelled else "DONE"
		self.logger.info(f"Print {str}")
		self.history.StopJob(cancelled)

	## on_after_startup
	def on_after_startup(self):
		# count
		self.count = 0
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
		historySize = self._settings.get(["historySize"])
		# history
		self.history = History(self.logger, self._settings.get_plugin_data_folder(), historySize)
		self.logger.info(f"START UP\n\t\t\t\tEnabled: '{enabled}'\n\t\t\t\tAutoclose: '{autoclose}'\n\t\t\t\tHistorySize: '{historySize}'")

	## on_event
	def on_event(self, event, payload):
		if self.isEnabled():
			if event == Events.PRINT_STARTED:
				self.printStarted(payload)
			elif event == Events.PRINT_DONE:
				self.printStopped(payload, False)
			elif event == Events.PRINT_FAILED:
				self.printStopped(payload, True)

	## isEnabled
	def isEnabled(self):
		return self._settings.get(["enabled"])

	@octoprint.plugin.BlueprintPlugin.route("/history", methods=["GET"])
	def getHistory(self):
		data = self.history.GetAll()
		return jsonify(data)

	##-- AssetPlugin hooks
	def get_assets(self):
		return dict(js=["js/IgnorePausedForUser.js"],
				    css=["css/style.css"])
		
	##-- Settings hooks
	def get_settings_defaults(self):
		return dict(enabled=False, autoclose=True, historySize=3)	
	
	##-- Template hooks
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]

	##-- Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			ignorepausedforuser=dict(
				displayName="IgnorePausedForUser",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="DavideM84",
				repo="OctoPrint-IgnorePausedForUser",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/DavideM84/OctoPrint-IgnorePausedForUser/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Ignore 'Paused for user'"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = IgnorePausedForUser()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.checkPausedForUser,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


# coding=utf-8

import octoprint.plugin
import re

class IgnorePausedForUser(octoprint.plugin.AssetPlugin,
						  octoprint.plugin.TemplatePlugin,
                		  octoprint.plugin.SettingsPlugin):
				
	def CheckPausedForUser(self, comm, line, *args, **kwargs):
		if "echo:busy: paused for user" in line:
			if self._settings.enabled:
				self._printer.commands("M103", tags=None, force=True)
				self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg="Ignored 'Paused for User'"))
		return line
	
	##-- AssetPlugin hooks
	def get_assets(self):
		return dict(js=["js/IgnorePausedForUser.js"])
		
	##-- Settings hooks
	def get_settings_defaults(self):
		return dict(enabled=False)	
	
	##-- Template hooks
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]
		
	##~~ Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			PrinterAlerts=dict(
				displayName="IgnorePausedForUser",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="DavideM84",
				repo="OctoPrint-IgnorePausedForUser",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/DavideM84/OctoPrint-IgnorePausedForUsers/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "IgnorePausedForUser"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = IgnorePausedForUser()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.CheckPausedForUser,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


# coding=utf-8

########################################################################################################################
### Do not forget to adjust the following variables to your own plugin.

# The plugin's identifier, has to be unique
plugin_identifier = "IgnorePausedForUser"

# The plugin's python package, should be "octoprint_<plugin identifier>", has to be unique
plugin_package = "octoprint_%s" % plugin_identifier

# The plugin's human readable name. Can be overwritten within OctoPrint's internal data via __plugin_name__ in the
# plugin module
plugin_name = "OctoPrint-%s" % plugin_identifier

# The plugin's version. Can be overwritten within OctoPrint's internal data via __plugin_version__ in the plugin module
plugin_version = "1.2.4"

# The plugin's description. Can be overwritten within OctoPrint's internal data via __plugin_description__ in the plugin
# module
plugin_description = "Simple plugin that sends M108 after receiving 'Paused for user' from the printer to resume printing immediately"

# The plugin's author. Can be overwritten within OctoPrint's internal data via __plugin_author__ in the plugin module
plugin_author = "Davide Mencarelli"

# The plugin's author's mail address.
plugin_author_email = "d.mencarelli@outlook.com"

# The plugin's homepage URL. Can be overwritten within OctoPrint's internal data via __plugin_url__ in the plugin module
plugin_url = "https://github.com/DavideM84/OctoPrint-IgnorePausedForUser"

# The plugin's license. Can be overwritten within OctoPrint's internal data via __plugin_license__ in the plugin module
plugin_license = "GPLv3"

# Any additional requirements besides OctoPrint should be listed here
plugin_requires = []

# Additional package data to install for this plugin. The subfolders "templates", "static" and "translations" will
# already be installed automatically if they exist.
plugin_additional_data = []

########################################################################################################################

from setuptools import setup

try:
	import octoprint_setuptools
except:
	print("Could not import OctoPrint's setuptools, are you sure you are running that under "
	      "the same python installation that OctoPrint is installed under?")
	import sys
	sys.exit(-1)

setup(**octoprint_setuptools.create_plugin_setup_parameters(
	identifier=plugin_identifier,
	name=plugin_name,
	version=plugin_version,
	description=plugin_description,
	author=plugin_author,
	mail=plugin_author_email,
	url=plugin_url,
	license=plugin_license,
	requires=plugin_requires,
	additional_data=plugin_additional_data
))

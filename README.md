# OctoPrint-IgnorePausedForUser

Octoprint plugin to ignore 'Paused for User' message from printer.  

Occasionally when printing from Octoprint the printer stuck with the message ''Paused for user".
I think it's a bug in the Marlin firmware, this plugin when receives the paused message from the printer, sends an M103 to resume printing immediately.  
Obviously it should not be used if one or more filament changes are planned.

### Settings

* Enable/Disabled  
To enable/disable the M103 response

### Changelog

* Version 1.1.0 25/01/2020  
First release

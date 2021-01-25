$(function() {
    function IgnorePausedForUserViewModel(parameters) {
        var self = this;
		
		self.settingsViewModel = parameters[0];
		
		self.enabled = ko.observable();

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "IgnorePausedForUser") {
				 console.log('Ignoring '+plugin);
                return;
            }
			
			if(data.type == "popup") {
				// console.log(data.msg);
				if(self.settingsViewModel.settings.plugins.IgnorePausedForUser.enabled)
				{
					new PNotify({
						title: 'IgnorePausedForUser',
						text: data.msg,
						type: "info",
						hide: true
						});
				}
			}
		}
		
		self.onBeforeBinding = function() {
            self.enabled(self.settingsViewModel.settings.plugins.IgnorePausedForUser.enabled());
        }
		
		self.onEventSettingsUpdated = function (payload) {            
            self.enabled = self.settingsViewModel.settings.plugins.IgnorePausedForUser.enabled();
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        IgnorePausedForUserViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#settings_plugin_IgnorePausedForUserViewModel_form"]
    ]);
});

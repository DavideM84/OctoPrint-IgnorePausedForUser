$(function() {
    function IgnorePausedForUserViewModel(parameters) {
        var self = this;
		
		self.settingsViewModel = parameters[0];
        self.enabled = ko.observable();
        self.autoclose = ko.observable();
        self.historySize = ko.observable();

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "IgnorePausedForUser") 
                return;

            if(self.settingsViewModel.settings.plugins.IgnorePausedForUser.enabled())
            {
                new PNotify({
                    title: '<p style="text-align:center">Paused for User</p>',
                    text: '\n' + data.msg,
                    type: "info",
                    hide: data.hide
                    });
            }
		}
		
		self.onBeforeBinding = function() {
            self.enabled(self.settingsViewModel.settings.plugins.IgnorePausedForUser.enabled());
            self.autoclose(self.settingsViewModel.settings.plugins.IgnorePausedForUser.autoclose());
            self.historySize(self.settingsViewModel.settings.plugins.IgnorePausedForUser.historySize());
        }
		
		self.onEventSettingsUpdated = function (payload) {            
            self.enabled = self.settingsViewModel.settings.plugins.IgnorePausedForUser.enabled();
            self.autoclose = self.settingsViewModel.settings.plugins.IgnorePausedForUser.autoclose();
            self.historySize = self.settingsViewModel.settings.plugins.IgnorePausedForUser.historySize();
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
        ["#settings_plugin_IgnorePausedForUser_form"]
    ]);
});

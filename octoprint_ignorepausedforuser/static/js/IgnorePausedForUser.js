$(function() {
    function IgnorePausedForUserViewModel(parameters) {
        var self = this;
		
		self.settingsViewModel = parameters[0];
        self.enabled = ko.observable();
        self.autoclose = ko.observable();
        self.historySize = ko.observable();
        self.historyData = ko.observable({"jobs": []});

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "ignorepausedforuser") 
                return;

            if(self.settingsViewModel.settings.plugins.ignorepausedforuser.enabled())
            {
                new PNotify({
                                title: '<p style="text-align:center">Paused for User</p>',
                                text: '\n' + data.msg,
                                type: "info",
                                hide: data.hide
                            });
            }
		};

        self.loadHistory = function(observable)
        {
            $.ajax({
                url: "./plugin/ignorepausedforuser/history",
                type: "GET",
                contentType: "application/json",
                dataType: "json",
                success: function(result)
                {
                    observable(result);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Unable to load history.  Status: " + textStatus + ".  Error: " + errorThrown);                    
                }
            });
        };

        self.StrDate = function(src)
        {
            var dt = new Date(src);
            var yyyy = dt.getFullYear();
            var MM = dt.getMonth() + 1;
            var dd = dt.getDay();
            var hh = dt.getHours();
            var mm = dt.getMinutes();
            return yyyy+"-"+MM+"-"+dd+" "+hh+":"+mm;
        };

		self.onBeforeBinding = function() 
        {
            self.enabled(self.settingsViewModel.settings.plugins.ignorepausedforuser.enabled());
            self.autoclose(self.settingsViewModel.settings.plugins.ignorepausedforuser.autoclose());
            self.historySize(self.settingsViewModel.settings.plugins.ignorepausedforuser.historySize());
        };
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
        [ "#ignorepaused_settings_container" ]
    ]);
});

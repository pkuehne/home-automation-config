import appdaemon.appapi as api
import datetime as dt

#
# Status Update app
#
# Args:
#


class Summary(api.AppDaemon):
    """ Creates a summary status for the house """

    def initialize(self):
        """ Set up callbacks etc """
        self.log("Summary initialised...")
        self.create_status()

    def create_status(self):
        """ Creates the status message """
        peter_home = self.get_state("device_tracker.peter_phone") == "home"
        peter_battery = self.get_state("device_tracker.peter_phone", "battery")
        current_time = dt.datetime.now().time()

        message = ""
        message += "Hello. It is currently " 
        message += "{} {}. ".format(current_time.hour, current_time.minute)

        message += "Peter is currently {}. ".format(
                    "at home" if peter_home else "not at home")
        self.log (message)

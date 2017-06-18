import appdaemon.appapi as api
import datetime as dt

#
# Light Control App
#
# Args:
#

class EveningOn(api.AppDaemon):
    """ Turns on couch light when it gets dark """

    def initialize(self):
        """ Sets up callbacks and state """
        # Sunset minus 45 minutes
        self.run_at_sunset(self.sunset_callback,
                            offset=dt.timedelta(minutes=-30).total_seconds())
        self.log("EveningOn initialised...")

    def sunset_callback(self, kwargs):
        """ Turn on lights """
        self.log("Checking whether to turn on the couch light...")
        if self.get_state("group.people") == "home":
            self.log("Someone's home...")
            self.turn_on("light.behind_couch",
                    brightness_pct=80,
                    transition=900)
            self.log("Turning on couch light...")

class NightOff(api.AppDaemon):
    """ Turns lights off when late and no activity """

    def initialize(self):
        """ Set up callbacks and state """

        self.log("NightOff initialised...")
        self.run_daily(self.night_check_callback, dt.time(22,0,0))

    def night_check_callback(self, kwargs):
        """ Callback to check for activity """
        self.log("Night time, activating check")
        self.run_in(self.activity_check_callback, 60)

    def activity_check_callback(self, kwargs):
        """ Callback runs periodically to check for activity """
        self.log("Checking for activity...")
        if self.get_state("media_player.living_room_tv") == "off":
            self.log("No activity. Turning off light...")
            self.turn_off("light.behind_couch", transition=900)
        else:
            if self.now_is_between("22:00:00", "03:00:00"):
                # Run check only until 3am
                self.log("Its between 22:00-03:00, running check in 60s...")
                self.run_in(self.activity_check_callback, 60)
            else:
                # It's past 3am, just turn it off
                self.turn_off("light.behind_couch")
                self.turn_off("media_player.living_room_tv")

class PatioLight(api.AppDaemon):
    """ Control the Patio Light """

    def initialize(self):
        """ Sets up callbacks and state """
        # Sunset minus 45 minutes
        self.run_at_sunset(self.sunset_callback)
        self.run_at_sunrise(self.sunrise_callback)
        self.log("PatioLight initialised...")

    def sunset_callback(self, kwargs):
        """ Turn the light on """
        self.turn_on("light.patio_light", brightness=254)
        self.log("Patio light turned on...")

    def sunrise_callback(self, kwargs):
        """ Turn the light off """
        self.log("Turning off patio light...")
        self.turn_off("light.patio_light")
        self.run_in(self.verification_callback, 10)

    def verification_callback(self, kwargs):
        """ Checks the light is actually off """
        patio_state = self.get_state("light.patio_light")
        if patio_state == "on":
            self.log("Patio light wasn't off yet, trying again...")
            self.turn_off("light.patio_light")
            self.run_in(self.verification_callback, 30)
        else:
            self.notify("Turned off patio light!", title="Home Assistant")

import appdaemon.appapi as api
import datetime as dt

#
# Motion Controlled lights
#
# Args:
#   - sensor
#   - light
#
# Use with:
# sensor: sensor.something
# light: light.something
# constrain_start_time = sunset + 00:30:00
# constrain_end_time = sunrise
#

class MotionLight(api.AppDaemon):
    """ Turns on couch light when it gets dark """

    def initialize(self):
        """ Sets up callbacks and state """
        self.handle = None
        self.log("Motion Lights initalised for '{}'".format(
            self.args["light"]))
        self.listen_state(self.motion_callback, self.args["sensor"], new = "on")
        self.listen_state(self.still_callback, self.args["sensor"], new = "off")

    def motion_callback(self, entity, attribute, old, new, kwargs):
        """ Motion detected """
        self.log("Motion detected")
        self.turn_on(self.args["light"], brightness_pct=self.args["brightness"])

    def still_callback(self, entity, attribute, old, new, kwargs):
        """ Motion has gone away """
        self.log("Motion has gone")
        self.turn_off(self.args["light"], transition=30)


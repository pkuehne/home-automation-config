import appdaemon.appapi as api
import datetime as dt

#
# Motion Controlled lights
#
# Args:
#   - sensor
#   - light
#

class MotionLight(api.AppDaemon):
    """ Turns on couch light when it gets dark """

    def initialize(self):
        """ Sets up callbacks and state """
        self.handle = None
        self.log("Motion Lights initalised...")
        self.listen_state(self.motion_callback, args["sensor"], new = "on")
        self.listen_state(self.still_callback, args["sensor"], new = "off")

    def motion_callback(self, kwargs):
        """ Motion detected """
        self.log("Motion detected")
        self.turn_on(args["light"], brightness_pct=args["brightness"])

    def still_callback(self, kwargs):
        """ Motion has gone away """
        self.log("Motion has gone")
        self.turn_off(args["light"], transition=60)


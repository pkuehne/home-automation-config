import appdaemon.appapi as api
import datetime as dt

#
# Temperature Controlled Fan
#
# Args:
#   - sensor
#   - fan
#
# Use with:
# sensor: sensor.something
# fan: switch.something
# upper_bound: 25
# lower_bound: 23
#
# Will trigger when temperature is > upper
# and turn off when temperature is < lower

class FanController(api.AppDaemon):
    """ Turns on fan when it gets hot """

    def initialize(self):
        """ Sets up callbacks and state """
        self.handle = None
        self.log("Fan Controller initalised...")
        self.listen_state(self.temperature_change_callback, self.args["sensor"])

    def temperature_change_callback(self, entity, attributes, old, new, kwargs):
        """ Temperature changed """
        if new is not None and new > self.args["upper_bound"]:
            self.log("It's too hot @ {}C, turning on {}".format(
                new, self.args["fan"]))
            self.turn_on(self.args["fan"])

        if new is not None and new < self.args["lower_bound"]:
            self.log("It's cold enough again @ {}C, turning off {}".format(
                new, self.args["fan"]))
            self.turn_off(self.args["fan"])


import appdaemon.appapi as api
import datetime as dt

class AlarmClock(api.AppDaemon):
    """ Morning alarm clock """

    def initialize(self):
        """ Sets up callbacks and state """
        self.wakeup_handle = None
        self.listen_state(self.wakeup_disabled,
                            "input_boolean.wakeup_enabled",
                            new="off")
        self.listen_state(self.wakeup_enabled,
                            "input_boolean.wakeup_enabled",
                            new="on")

    def wakeup_enabled(self, entity, attributes, old, new, kwargs):
        """ Set a timer based on the slider inputs """
        hour = self.get_state("input_slider.wakeup_hour")
        minute = self.get_state("input_slider.wakeup_minute")
        timer = dt.time(int(float(hour)),int(float(minute)),0)
        self.wakeup_handle = self.run_daily(self.wakeup_callback, timer)
        self.log("Wakeup timer enabled for {}".format(timer))

    def wakeup_disabled(self, entity, attributes, old, new, kwargs):
        """ Cancel the timer if it is set """
        if self.wakeup_handle is not None:
            self.cancel_timer(self.wakeup_handle)
            self.log("Wakeup timer cancelled")

    def wakeup_callback(self, kwargs):
        """ Called in the morning to do stuff """
        self.log ("Good morning")
        # Turn on morning light
        # Schedule status message
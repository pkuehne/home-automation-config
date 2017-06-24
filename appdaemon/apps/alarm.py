import appdaemon.appapi as api
import datetime as dt

#
# Alarm App
#
# Args:
#

class AlarmController(api.AppDaemon):
    """ Looks after the alarm system """

    def initialize(self):
        """ Sets up callbacks and state """
        self.log("Alarm Controller initialised...")
        self.listen_state(self.alarm_trigger, "group.motion_detectors", new = "on")
        #self.listen_state(self.alarm_trigger, "group.door_sensors", new = "on")

    def alarm_trigger(self, entity, attribute, old, new, kwargs):
        self.log("A change was detected")
        if self.get_state("alarm_control_panel.ha_alarm") != "disarmed":
            self.log("Triggering the alarm")
            self.notify("Entity {} triggered the alarm".format(
                entity if entity is not None else "<Unknown>"),
                title="Home Assistant")
            self.call_service ("alarm_control_panel/alarm_trigger",
                    entity_id = entity)


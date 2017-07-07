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

    def alarm_trigger(self, trigger_group, attribute, old, new, kwargs):
        """ Called when there is a change """
        triggered_sensor = None
        for sensor in self.get_state(trigger_group, "all")["attributes"]["entity_id"]:
            if self.get_state(sensor) == "on":
                # This one triggered the alarm
                triggered_sensor = sensor
                break

        if self.get_state("alarm_control_panel.ha_alarm") != "disarmed":
            self.log("Triggering the alarm")
            # This could be moved to the trigger-reaction code
            if triggered_sensor is not None:
                sensor_name = self.get_state(triggered_sensor, "friendly_name")
            else:
                sensor_name = "Unknown"
            self.notify("Entity <{}> triggered the alarm".format(sensor_name),
                title="Home Assistant")
            self.call_service ("alarm_control_panel/alarm_trigger",
                    entity_id = triggered_sensor)


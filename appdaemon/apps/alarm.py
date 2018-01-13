import datetime as dt
import appdaemon.plugins.hass.hassapi as hass


#
# Alarm App
#
# Args:
#

class AlarmController(hass.Hass):
    """ Looks after the alarm system """

    def initialize(self):
        """ Sets up callbacks and state """
        self.log("Alarm Controller initialised...")
        self.listen_state(self.upstairs_motion, "group.upstairs_motion_sensors", new = "on")
        self.listen_state(self.downstairs_motion, "group.downstairs_motion_sensors", new = "on")
        self.listen_state(self.door_opened, "group.door_sensors", new = "on")
        self.listen_state(self.alarm_triggered, "alarm_control_panel.alarm_status", new = "triggered")

        self.listen_state(self.everyone_away, "group.people", new = "not_home")
        self.listen_state(self.someone_home, "group.people", new = "home")

    def upstairs_motion(self, trigger_group, attribute, old, new, kwargs):
        """ Triggers if armed away and there's motion """
        alarm_status = self.get_state("alarm_control_panel.alarm_status")
        if alarm_status == "armed_away":
            self.log ("Alarm! Detected motion upstairs")
            self.trigger_alarm(trigger_group)

    def downstairs_motion(self, trigger_group, attribute, old, new, kwargs):
        """ Triggers if armed home or away and downstairs should be checked """
        alarm_status = self.get_state("alarm_control_panel.alarm_status")
        check_downstairs = \
            self.get_state("input_boolean.check_downstairs_motion_sensors")
        if alarm_status == "armed_away" and check_downstairs == "on":
            self.log ("Alarm! Detected motion downstairs")
            self.trigger_alarm(trigger_group)
        if alarm_status == "armed_home" and check_downstairs == "on":
            self.log ("Alarm! Detected motion downstairs")
            self.trigger_alarm(trigger_group)

    def door_opened(self, trigger_group, attribute, old, new, kwargs):
        """ Triggers if armed away and there's motion """
        alarm_status = self.get_state("alarm_control_panel.alarm_status")
        if alarm_status == "armed_away":
            self.log ("Alarm! Detected door opened")
            self.trigger_alarm(trigger_group)
        if alarm_status == "armed_home":
            self.log ("Alarm! Detected door opened")
            self.trigger_alarm(trigger_group)

    def trigger_alarm(self, group):
        """ Called when the alarm should be triggered """
        triggered_sensor = None
        sensors = self.get_state(group, "all")["attributes"]["entity_id"]
        for sensor in sensors:
            if self.get_state(sensor) == "on":
                # This one triggered the alarm
                triggered_sensor = sensor
                break

        self.log("Triggering the alarm")
        if triggered_sensor is not None:
            sensor_name = self.get_state(triggered_sensor, "friendly_name")
        else:
            sensor_name = "Unknown"
        self.fire_event ("NOTIFY",
                message = "Entity <{}> triggered the alarm".format(sensor_name))
        self.fire_event ("NOTIFY",
                message = "Unauthorized entry detected!",
                announce = True)

    def alarm_triggered(self, entity, attribute, old, new, kwargs):
        """ Called when the alarm panel is triggered in some way """
        self.log ("The alarm was triggered")

    def everyone_away(self, entity, attribute, old, new, kwargs):
        """ Called when everyone has left - set the alarm """
        auto_arm = self.get_state("input_boolean.control_alarm_automatically")
        alarm_status = self.get_state("alarm_control_panel.alarm_status")
        if auto_arm == "on" and alarm_status == "disarmed":
            self.log ("Everyone away - setting alarm")
            self.call_service ("alarm_control_panel/alarm_arm_away",
                    entity_id = "alarm_control_panel.alarm_status")

    def someone_home(self, entity, attribute, old, new, kwargs):
        """ Called when someone has returned - disarm the alarm """
        auto_disarm = self.get_state("input_boolean.control_alarm_automatically")
        alarm_status = self.get_state("alarm_control_panel.alarm_status")
        if auto_disarm == "on" and alarm_status != "disarmed":
            self.log ("Someone returned - disarming alarm")
            self.call_service ("alarm_control_panel/alarm_disarm",
                    entity_id = "alarm_control_panel.alarm_status")


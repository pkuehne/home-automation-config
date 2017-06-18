import appdaemon.appapi as api
import datetime as dt

#
# Device Control App
#
# Args:
#

class NotifyOnNewDevice(api.AppDaemon):
    """ Turns on couch light when it gets dark """

    def initialize(self):
        """ Sets up callbacks and state """
        self.log("Device sniffer initialised...")
        self.listen_event(self.new_device_callback, "device_tracker_new_device")

    def new_device_callback(self, event_name, data, kwargs):
        self.log("New device detected")
        self.log(data)
        self.notify("New device '{}' detected on network".format(
            data["host_name"]),
            title="Home Assistant")


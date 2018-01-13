import appdaemon.plugins.hass.hassapi as hass
import datetime as dt

class Summary(hass.Hass):
    """ Creates a summary status for the house """

    def initialize(self):
        """ Set up callbacks etc """
        self.log("Summary initialised...")
        self.fire_event("NOTIFY",
                message=self.create_status(),
                announce=False)

    def notify_peter(self, kwargs):
        """ Tell Peter the status """
        self.notify(self.create_status(), title="Home Assistant")

    def create_status(self):
        """ Creates the status message """
        peter_home = self.entities.device_tracker.peter_phone.state == "home"
        peter_battery = self.entities.device_tracker.peter_phone.attributes.get("battery", 0)
        temperature = self.entities.sensor.average_temperature
        weather = self.entities.sensor.owm_condition
        current_time = dt.datetime.now().time()

        forecast = self.entities.weather.forecast.attributes.get("forecast", "None")
        high = max([forecast["temperature"] for forecast in forecast])
        low = min([forecast["temperature"] for forecast in forecast])

        message = ""
        message += "Hello. It is currently "
        message += "{} {}. ".format(current_time.hour, current_time.minute)

        #message += "Peter is {}. ".format(
        #            "at home" if peter_home else "not at home")

        message += "The average temperature in the house is " \
                    "{} degrees. ".format(temperature)

        message += "The weather is {} ".format(weather)
        message += "with a forecast high of {} degrees " \
                "and a low of {} degrees".format(high, low)
        return message

    def format_temperature(temperature):
        """ From 3.69 -> 3 point 6 9 """


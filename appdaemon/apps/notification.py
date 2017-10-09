import appdaemon.appapi as api

# Use with
#   self.fire_event ("NOTIFY",
#                    message="a message",
#                    announce=False, # Announce over Sonos or send as message
#                    recipients=["peter_phone"], # list of mqtt recipients
#                    speaker="media_player.kitchen", # Sonos player to play on
#                   )
class Notify(api.AppDaemon):
    """ Notify people of something """

    def initialize(self):
        """ Sets up callbacks and state """
        self.listen_event(self.notify_event, "NOTIFY")

    def notify_event(self, event_name, data, kwargs):
        """ A new notification was received """
        default_recipients = ["peter_phone", "ro_phone"]
        message = data.get("message", "A fault occurred")
        announce = data.get("announce", False)
        speakers = data.get("speakers", "media_player.living_room")
        recipients = data.get("recipients", default_recipients)

        if announce:
            sonos_message = "This is Home Assistant, " + message
            sonos_delay = len(sonos_message) / 10.0 # 1 sec per 10 letters ish
            self.fire_event ("SONOS_SAY",
                     speaker=speakers,
                     message=sonos_message,
                     delay=sonos_delay)
        else:
            for recipient in recipients:
                self.call_service("mqtt/publish",
                        topic="zanzito/{}/notification".format(recipient),
                        payload=message)



import appdaemon.plugins.hass.hassapi as hass

# Use with
#   self.fire_event ("SONOS_SAY",
#                    speaker="media_player.den",
#                    message="test message",
#                    delay=5.0)
#

class SonosSay(hass.Hass):
    """ Make Sonos say something """

    def initialize(self):
        """ Sets up callbacks and state """
        self.listen_event(self.sonos_say_event, "SONOS_SAY")

    def sonos_say_event(self, event_name, data, kwargs):
        """ Says stuff over Sonos """

        #self.log(", ".join("=".join(_) for _ in data.items()))
        player_volume = 0.3
        player_entity = data.get("speaker", "media_player.kitchen")
        player_message = data.get("message", "This is Home Assistant, I experienced an internal fault")
        player_delay = data.get("delay", 5.0)
        self.call_service ("media_player/sonos_snapshot",
                            entity_id=player_entity)
        self.call_service ("media_player/sonos_unjoin",
                            entity_id=player_entity)
        self.call_service ("media_player/volume_set",
                            entity_id=player_entity,
                            volume_level=player_volume)
        self.call_service ("tts/google_say",
                            entity_id=player_entity,
                            message=player_message)
        self.log ("Waiting {}s".format(player_delay))
        self.run_in (self.sonos_restore, player_delay, player_entity=player_entity)

    def sonos_restore(self, kwargs):
        """ Restores the speaker back """
        self.call_service ("media_player/sonos_restore",
                            entity_id=kwargs["player_entity"])


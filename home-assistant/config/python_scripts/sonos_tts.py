import time

message = data.get('message', "Hello from your Sonos!")
volume = data.get('volume', 0.2)
delay = data.get('delay', 5.0)
sonos_entity = data.get('sonos_entity', None)
if sonos_entity is None:
    #return
    sonos_entity = "media_player.den"

logger.info("Snapshot")
# Capture what the sonos is doing right now
hass.services.call ('media_player', 'sonos_snapshot',
        service_data={"entity_id": sonos_entity})

logger.info("unjoin")
# Take it out of any groups
hass.services.call ('media_player', 'sonos_unjoin',
        service_data={"entity_id": sonos_entity})

logger.info("volume")
# Set a good volume to be heard
hass.services.call ('media_player', 'volume_set',
        service_data={"entity_id": sonos_entity, "volume": volume})

logger.info("say")
# Say what you have to say
hass.services.call ('tts', 'google_say',
        service_data={"entity_id": sonos_entity, "message": message},
        blocking=True)

logger.info("sleep")
# Wait for the message to be passed
time.sleep(delay)

logger.info("restore")
# Now put it back to how it was
hass.services.call ('media_player', 'sonos_restore',
        service_data={"entity_id": sonos_entity})

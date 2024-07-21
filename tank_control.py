# tank_control.py
import time
import threading
from paho.mqtt import client as mqtt_client

class TankControl:
    def __init__(self, mqtt_client):
        self.level = 0
        self.mqtt_client = mqtt_client
        self.publish_thread = threading.Thread(target=self.publish_level_periodically)
        self.publish_thread.daemon = True
        self.publish_thread.start()

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    def publish_level_periodically(self):
        while True:
            self.mqtt_client.publish("tank/levels", str(self.level))
            time.sleep(5)  # Publish every 5 seconds
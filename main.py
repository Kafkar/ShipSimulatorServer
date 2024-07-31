# main.py
import paho.mqtt.client as mqtt

import configparser

from flask import Flask, render_template, request, jsonify
from routes import register_all_routes
from tank_control import TankControl
from log_processor import LogProcessor

app = Flask(__name__)

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')


# MQTT setup
mqtt_client = mqtt.Client()

# Set username and password
mqtt_client.username_pw_set(
    config['MQTT']['username'],
    config['MQTT']['password']
)

mqtt_client.connect(
    config['MQTT']['broker_address'],
    int(config['MQTT']['broker_port']),
    int(config['MQTT']['keep_alive'])
)
mqtt_client.loop_start()

# Create and start LogProcessor
log_processor = LogProcessor(mqtt_client, config)
log_processor.start()

# Create TankControl instance
tank_control = TankControl(mqtt_client)
register_all_routes(app, tank_control) 

mqtt_client.publish("topic/test", "Hello, MQTT!")


def on_message(client, userdata, message):
    print(f"Received message '{str(message.payload.decode('utf-8'))}' on topic '{message.topic}'")

mqtt_client.on_message = on_message
mqtt_client.subscribe("topic/#")
mqtt_client.subscribe("tank/levels")


if __name__ == '__main__':
    app.run(debug=True)
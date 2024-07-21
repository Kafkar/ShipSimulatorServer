# main.py
import paho.mqtt.client as mqtt

from flask import Flask, render_template, request, jsonify
from routes import register_all_routes
from tank_control import TankControl

app = Flask(__name__)

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)  # Replace with your MQTT broker address and port
mqtt_client.loop_start()

# Create TankControl instance
tank_control = TankControl(mqtt_client)
register_all_routes(app, tank_control) 

# mqtt_client.publish("topic/test", "Hello, MQTT!")


def on_message(client, userdata, message):
    print(f"Received message '{str(message.payload.decode('utf-8'))}' on topic '{message.topic}'")

mqtt_client.on_message = on_message
# mqtt_client.subscribe("topic/#")
mqtt_client.subscribe("tank/levels")


if __name__ == '__main__':
    app.run(debug=True)
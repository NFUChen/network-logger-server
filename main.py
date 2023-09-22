
from logging.handlers import TimedRotatingFileHandler
import logging
import time
import paho.mqtt.client as mqtt
import json
# Create a custom log file name based on the current date
current_date = time.strftime("%Y-%m-%d")
log_filename = f"./log/{current_date}.log"

# Configure the logging settings with a custom log file name
log_formatter = logging.Formatter('%(asctime)s - %(message)s')
log_handler = TimedRotatingFileHandler(filename=log_filename, when='midnight', interval=1)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode('utf-8'))
    logger.info(payload)

# Define the MQTT broker address and port
broker_address = "10.3.5.60"
broker_port = 1883  # Default MQTT port

# Create an MQTT client
client = mqtt.Client()

# Set the callback function for incoming messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Subscribe to the topic where log messages are being published
topic = "network/#"
client.subscribe(topic)

# Start the MQTT client loop to listen for incoming messages
client.loop_forever()
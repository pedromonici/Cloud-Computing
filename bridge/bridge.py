from paho.mqtt import client as mqtt_client
from kafka import KafkaProducer
import time
import logging
import sys
import os

logging.basicConfig(
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class MosquittoMessageSubscriber:
    def __init__(self, uri, port, topic):
        def subscribe_handler(client, obj, mid, granted_qos):
            logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))

        def connection_handler(client, userdata, flags, rc):
            if rc == 0:
                logging.info(f"Connected to MQTT broker {uri}.")
            else:
                raise Exception(f"Failed to connect to MQTT broker {uri} (return code {rc}).")

        self.client = mqtt_client.Client()
        self.client.on_connect = connection_handler
        self.client.on_subscribe = subscribe_handler
        self.topic = topic
        self.uri = uri
        self.port = port
        self.handler_was_set = False

    def set_message_handler(self, handler):
        def wrapped_handler(client, userdata, msg):
            logging.info(f"Received {msg.payload.decode()} from {msg.topic} topic.")
            handler(msg.payload.decode())
        self.client.on_message = wrapped_handler
        self.handler_was_set = True

    def run(self):
        if not self.handler_was_set:
            raise Exception("Message handler must be set before running the mosquitto client")
        logging.info("Bridge process started successfully.")
        self.client.connect(self.uri, self.port)
        self.client.subscribe(self.topic)
        self.client.loop_forever()

class KafkaMessageProducer:
    def __init__(self, uri, port, topic):
        self.client = KafkaProducer(bootstrap_servers=f"{uri}:{port}")
        self.topic = topic

    def send_message(self, msg):
        future = self.client.send(self.topic, bytes(msg, 'utf-8'))
        result = future.get(timeout=10)
        logging.info(f"Wrote a message of size {result.serialized_value_size} to the Kafka log offset {result.offset}.")

if __name__ == "__main__":
    logging.info("Loading bridge configs.")
    mqtt_config = {
        "uri": os.environ["MQTT_URI"],
        "port": int(os.environ["MQTT_PORT"]),
        "topic": os.environ["MQTT_TOPIC"],
    }
    kafka_config = {
        "uri": os.environ["KAFKA_URI"],
        "port": int(os.environ["KAFKA_PORT"]),
        "topic": os.environ["KAFKA_TOPIC"]
    }
    logging.info("Starting bridge process.")
    producer = KafkaMessageProducer(**kafka_config)
    mosquitto_client = MosquittoMessageSubscriber(**mqtt_config)
    mosquitto_client.set_message_handler(producer.send_message)
    mosquitto_client.run()

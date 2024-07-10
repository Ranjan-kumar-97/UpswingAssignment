import pika
import json
import threading
from pymongo.collection import Collection
from ConnectMongo import collection
from Configurations import Config


class RabbitMQState:
    """
    A class to maintain the state of the RabbitMQ connection and channel.

    Attributes:
        connection (pika.BlockingConnection): The RabbitMQ connection.
        channel (pika.adapters.blocking_connection.BlockingChannel): The RabbitMQ channel.
    """
    def __init__(self):
        """
        Initialize the RabbitMQState with None for connection and channel.
        """
        self.connection = None
        self.channel = None

rabbitmq_state = RabbitMQState()

def consume():
    """
    Start the RabbitMQ consumer that listens for messages on the 'mqtt_queue'.

    This function establishes a connection to RabbitMQ, declares a queue, and starts consuming messages.
    """
    print("Starting RabbitMQ consumer")
    params = pika.URLParameters(Config.RABBITMQ_URL)
    rabbitmq_state.connection = pika.BlockingConnection(params)
    rabbitmq_state.channel = rabbitmq_state.connection.channel()
    rabbitmq_state.channel.queue_declare(queue='mqtt_queue')
    rabbitmq_state.channel.basic_consume(queue='mqtt_queue', on_message_callback=callback, auto_ack=True)
    print("RabbitMQ consumer started")
    try:
        rabbitmq_state.channel.start_consuming()
    except KeyboardInterrupt:
        rabbitmq_state.channel.stop_consuming()
    finally:
        if rabbitmq_state.connection:
            rabbitmq_state.connection.close()

def callback(ch, method, properties, body):
    """
    Callback function to process received messages from RabbitMQ.

    This function decodes the message from JSON, prints it, and stores it in MongoDB.

    Args:
        ch: The channel.
        method: The delivery method.
        properties: The properties.
        body: The message body.
    """
    try:
        message = json.loads(body)
        print(f"Received message from RabbitMQ: {message}")
        store_message_in_mongodb(message)
    except Exception as e:
        print(f"Error processing message: {e}")

def store_message_in_mongodb(message: dict):
    """
    Store a message in MongoDB.

    This function inserts the message into the MongoDB collection and prints a confirmation.

    Args:
        message (dict): The message to be stored.
    """
    try:
        collection.insert_one(message)
        print("Message stored in MongoDB")
    except Exception as e:
        print(f"Error storing message in MongoDB: {e}")

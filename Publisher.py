import pika
import json
import random
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# RabbitMQ Configuration
RABBITMQ_URL = os.getenv("CLOUDAMQP_URL")
params = pika.URLParameters(RABBITMQ_URL)

def publish_messages():
    """
    Publish MQTT messages with random status to a RabbitMQ queue.

    This function connects to RabbitMQ using the URL specified in the environment
    variables, declares a queue named 'mqtt_queue', and continuously publishes
    messages with a random status and the current timestamp to this queue.

    The function will keep running and publishing messages every second until
    interrupted by the user (e.g., by pressing Ctrl+C).

    Raises:
        KeyboardInterrupt: To stop the message publishing and close the connection.
    """
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='mqtt_queue')

    try:
        while True:
            status = random.randint(0, 6)
            message = json.dumps({"status": status, "timestamp": int(time.time())})
            channel.basic_publish(exchange='', routing_key='mqtt_queue', body=message)
            print(f"Message published to RabbitMQ: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        connection.close()

if __name__ == '__main__':
    publish_messages()

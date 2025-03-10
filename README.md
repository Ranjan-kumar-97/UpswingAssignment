# FastAPI RabbitMQ and MongoDB Integration

This Project is made as an assignment of Upswing to develop a client-server script in Python that handles MQTT messages via RabbitMQ. The client script should emit MQTT messages every second containing a field "status" with a random value in the range of 0-6. The server should process these messages and store them in MongoDB. Additionally, the server should provide an endpoint to accept start and end times and return the count of each status during the specified time range.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

## Installation

1. Clone the repository:
    git clone https://github.com/Ranjan-kumar-97/UpswingAssignment.git


2. Create a virtual environment and activate it:
    python -m venv environment
    environment\Scripts\activate  # On Windows
    

3. Install the dependencies:
    pip install -r requirements.txt

4. Set up environment variables by creating a `.env` file in the root directory with the following content:

- `CLOUDAMQP_URL`: Your RabbitMQ CloudAMQP URL
- `MQTT_BROKER`: Your MQTT Broker
- `MQTT_PORT`: MQTT Port Number
- `MQTT_TOPIC`: MQTT Answer Topic
- `MQTT_USERNAME`: Your MQTT username
- `MQTT_PASSWORD`: Your MQTT username

- `MONGODB_USERNAME`: Your MongoDB username
- `MONGODB_PASSWORD`: Your MongoDB password
- `MONGODB_CLUSTER`: Your MongoDB cluster address
- `MONGODB_DBNAME`: Your MongoDB database name
- `MONGODB_COLLECTION`: Your MongoDB collection name

## Usage

1. Start the FastAPI server:
    uvicorn Server:Server --host 0.0.0.0 --port 8000

2. Start publishing messages to RabbitMQ:
    python publisher.py

3. The server will start consuming messages from RabbitMQ and storing them in MongoDB.

## API Endpoints

### POST /status_counts

Retrieves the count of each status within a specified time range.

- **Request Body**:
    ```json
    {
        "start_time": "2024-06-10T00:00:00",
        "end_time": "2024-07-12T00:00:00"
    }
    ```
  The `start_time` and `end_time` can be provided in various formats (date_formats like
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S").

- **Response**:
    ```json
    {
        "0": 5,
        "1": 10,
        "2": 7,
        "3": 3,
        "4": 8,
        "5": 2,
        "6": 1
    }
    ```
## Environment Variables

Ensure you have the following environment variables set in your `.env` file:

- `CLOUDAMQP_URL`: Your RabbitMQ CloudAMQP URL
- `MQTT_BROKER`: Your MQTT Broker
- `MQTT_PORT`: MQTT Port Number
- `MQTT_TOPIC`: MQTT Answer Topic
- `MQTT_USERNAME`: Your MQTT username
- `MQTT_PASSWORD`: Your MQTT username

- `MONGODB_USERNAME`: Your MongoDB username
- `MONGODB_PASSWORD`: Your MongoDB password
- `MONGODB_CLUSTER`: Your MongoDB cluster address
- `MONGODB_DBNAME`: Your MongoDB database name
- `MONGODB_COLLECTION`: Your MongoDB collection name


## Project Structure

UpswingAssignment/
│
├── .env # Environment variables
├── ConnectMongo.py # MongoDB connection setup
├── Consumer.py # RabbitMQ consumer logic
├── Models.py # Pydantic models and validation
├── Server.py # FastAPI server setup
├── StatusCounts.py # Endpoint logic for status counts
├── publisher.py # RabbitMQ message publisher script
├── requirements.txt # Python dependencies
└── README.md # Project documentation

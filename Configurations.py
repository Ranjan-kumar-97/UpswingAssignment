import os
from dotenv import load_dotenv

# Load environment variables from a .env file into the environment.
load_dotenv()

class Config:
    """
    A configuration class for loading and storing application settings from environment variables.

    Attributes:
        MONGODB_USERNAME (str): MongoDB username retrieved from the environment variable.
        MONGODB_PASSWORD (str): MongoDB password retrieved from the environment variable.
        MONGODB_CLUSTER (str): MongoDB cluster address retrieved from the environment variable.
        MONGODB_DBNAME (str): MongoDB database name retrieved from the environment variable.
        MONGODB_COLLECTION (str): MongoDB collection name retrieved from the environment variable.
        RABBITMQ_URL (str): RabbitMQ URL retrieved from the environment variable.
    """

    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
    MONGODB_CLUSTER = os.getenv("MONGODB_CLUSTER")
    MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")
    MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")
    RABBITMQ_URL = os.getenv("CLOUDAMQP_URL")

    @classmethod
    def mongodb_uri(cls):
        """
        Constructs the MongoDB URI using the stored configuration.

        Returns:
            str: A MongoDB connection string constructed from the username, password, cluster, and database name.
        """
        from urllib.parse import quote_plus
        username = quote_plus(cls.MONGODB_USERNAME)
        password = quote_plus(cls.MONGODB_PASSWORD)
        return f"mongodb+srv://{username}:{password}@{cls.MONGODB_CLUSTER}.l1lqtso.mongodb.net/{cls.MONGODB_DBNAME}?retryWrites=true&w=majority&appName=UpswingAssignment"

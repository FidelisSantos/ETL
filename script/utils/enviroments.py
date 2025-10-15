import os
from dotenv import load_dotenv

load_dotenv()
class Enviroments:
    STANDARD_MYSQL_URL = os.getenv("STANDARD_MYSQL_URL")
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    JOHN_DEERE_MYSQL_URL = os.getenv("JOHN_DEERE_MYSQL_URL")

    def __init__(self):
        self.STANDARD_MYSQL_URL = os.getenv("STANDARD_MYSQL_URL")
        self.JOHN_DEERE_MYSQL_URL = os.getenv("JOHN_DEERE_MYSQL_URL")
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.MONGO_DATABASE = os.getenv("MONGO_DATABASE")


env = Enviroments()
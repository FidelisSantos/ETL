import os
from dotenv import load_dotenv

load_dotenv()

class Enviroments:
    def __init__(self):
        self.STANDARD_MYSQL_URL = os.getenv("STANDARD_MYSQL_URL")
        self.JOHN_DEERE_MYSQL_URL = os.getenv("JOHN_DEERE_MYSQL_URL")
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.MONGO_DATABASE = os.getenv("MONGO_DATABASE")
        self.DIFF_TYPE = os.getenv("DIFF_TYPE", "days")
        self.OFFSET = int(os.getenv("OFFSET", 30))
        self.JOB_SLEEP_SECONDS = int(os.getenv("JOB_SLEEP_SECONDS", 60))
        self.JOB_REALTIME_SLEEP_SECONDS = int(os.getenv("JOB_REALTIME_SLEEP_SECONDS", 60))

env = Enviroments()
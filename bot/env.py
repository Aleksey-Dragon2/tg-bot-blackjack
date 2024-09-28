from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN", "")
SUPERUSERS = os.getenv("SUPERUSERS", "").split(",")

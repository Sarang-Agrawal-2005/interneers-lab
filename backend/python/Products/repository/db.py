import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

connect(
    db=os.getenv("MONGO_DB"),
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASS"),
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    authentication_source="admin"
)
from mongoengine import connect

connect(
    db="inventory",
    username="root",
    password="example",
    host="localhost",
    port=27019,
    authentication_source="admin"
)
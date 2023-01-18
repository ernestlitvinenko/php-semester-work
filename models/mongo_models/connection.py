from mongoengine import connect
from config import CONFIG


async def connect_db() -> None:
    print(CONFIG.database_name, CONFIG.mongo_conn_string)
    connect(db=CONFIG.database_name, host=CONFIG.mongo_conn_string)

from motor import motor_asyncio

def database_init(connection_string: str) -> motor_asyncio.AsyncIOMotorClient:    
    client = motor_asyncio.AsyncIOMotorClient(connection_string)
    return client


from os import environ
import uvicorn
from fastapi import FastAPI
from database import database_init
from dotenv import load_dotenv
app = FastAPI()

# On startup
@app.on_event('startup')
def statrup_handler():
    load_dotenv('development.env')
    print("Connection string is", environ.get('MONGO_DB_CONNECTION_STRING'))
    
    # set attribute database for app var  

    setattr(app, 'database',  database_init(environ.get('MONGO_DB_CONNECTION_STRING', '')))

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1')
            

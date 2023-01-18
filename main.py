import uvicorn

from users.views import router as user_router
from fastapi import FastAPI
from models.mongo_models.connection import connect_db
from loguru import logger
from config import CONFIG


logger.add(CONFIG.log_file, level='DEBUG', serialize=True)

app = FastAPI()
app.include_router(user_router)


@app.on_event('startup')
async def startup():
    try:
        await connect_db()
        print("Connection to DB successed")
    except Exception as exc:
        print(exc)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)

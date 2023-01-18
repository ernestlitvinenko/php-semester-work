from fastapi_jwt import JwtAccessBearer
from config import CONFIG
access_security = JwtAccessBearer(secret_key=CONFIG.secret_key, auto_error=True)

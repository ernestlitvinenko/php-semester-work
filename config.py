from pydantic import BaseSettings, MongoDsn
import subprocess
# Flag for development usage
DEVELOPMENT = True


def get_secret_key() -> str:
    return subprocess.run(
        ['openssl', 'rand', '-hex', '32'], stdout=subprocess.PIPE, text=True
    ).stdout


class Settings(BaseSettings):
    """
    Base Config Class
    """
    mongo_conn_string: MongoDsn = "mongodb://root:root@127.0.0.1:27017/"
    database_name: str = 'backend_dev'
    log_file: str = 'logs/log_{time:DD-MM-YYYY}.log'
    secret_key: str = get_secret_key()

    class Config:
        env_file = '.env' if not DEVELOPMENT else 'development.env'
        fields = {
            "mongo_conn_string": {
                'env': ['MONGO_DB_CONNECTION_STRING', 'mongo_conn_string']
            },
            "database_name": {
                'env': ['MONGO_DB_DATABASE_NAME', 'database_name']
            },
            'log_file': {
                'env': ['LOG_FILE', 'log_file']
            },
            'secret_key': {
                'env': ['SECRET_KEY', 'secret_key']
            }
        }


# Usage: from config import CONFIG
CONFIG = Settings()

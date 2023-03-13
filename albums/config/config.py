from albums.utils.utils import get_env_variable

POSTGRES_URL = get_env_variable('POSTGRES_URL')
POSTGRES_USER = get_env_variable('POSTGRES_USER')
POSTGRES_PW = get_env_variable('POSTGRES_PW')
POSTGRES_DB = get_env_variable('POSTGRES_DB')
DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'

JWT_SECRET_KEY = get_env_variable('JWT_SECRET_KEY')
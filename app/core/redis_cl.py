from redis import Redis
from dotenv import load_dotenv

load_dotenv()

redis_client = Redis(
    host='localhost',
    port=6379,
    db=0
)

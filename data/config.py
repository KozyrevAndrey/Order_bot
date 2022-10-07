import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=str(os.getenv("BOT_TOKEN"))
PGUSER=str(os.getenv("PGUSER"))
PGPASSWORD=str(os.getenv("PGPASSWORD"))
DATABASE=str(os.getenv("DATABASE"))
admins = [
    223993433,
    401089055
]

ip = os.getenv("ip")


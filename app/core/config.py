import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file into OS environment

DATABASE_URL = os.getenv("DATABASE_URL") # Get database connection URL from environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

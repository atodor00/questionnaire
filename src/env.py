# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file


load_dotenv("../config/.env") 
print(os.getenv("ADMIN_USER_USERNAME"))
print(os.getenv("ADMIN_USER_PASSWORD"))
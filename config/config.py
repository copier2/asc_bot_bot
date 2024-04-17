import os

import psycopg2
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

sql_connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
cursor = sql_connection.cursor()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

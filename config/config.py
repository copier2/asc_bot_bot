import os

import psycopg2
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

DP = Dispatcher()

# Переменные для подключения к БД
SQL_CONNECTION = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

CURSOR = SQL_CONNECTION.cursor()

# Счётчик количества записей брендов из БД
brand_select_count_query = f"""SELECT count(*) FROM asclist_brand;"""
CURSOR.execute(brand_select_count_query)
BRAND_COUNT_RECORDS = CURSOR.fetchone()[0]

# Счётчик количества записей АСЦ из БД
asc_select_count_query = f"""SELECT count(*) FROM asclist_asc;"""
CURSOR.execute(asc_select_count_query)
ASC_COUNT_RECORDS = CURSOR.fetchone()[0]

# Токен бота для входящих/исходящих сообщений
BOT = Bot(token=os.getenv('BOT_TOKEN'))

# Последняя дата обновления БД по АСЦ
UPDATE_DATE_BD = '25/04/2024'

# Текущая версия бота
BOT_VERSION = 'v1.1'

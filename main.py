import asyncio

from aiogram import F
from aiogram.types import Message

from config import config


@config.dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.first_name}, я твой виртуальный помощник'
    )


@config.dp.message()
async def get_text_bd(message: Message):
    brand_keys = message.text
    try:
        # Поиск id бренда по введенному запросу
        brand_select_query = f"""SELECT * FROM asclist_brand WHERE title='{brand_keys}';"""
        config.cursor.execute(brand_select_query)
        brand_records = config.cursor.fetchone()
        id_brands = brand_records[0]
        flag_cd_brand = brand_records[2]
        print(f'Для запроса "{brand_keys}" с id "{id_brands}:"')

        # Поиск записей в списке АСЦ по id бренда
        asclist_select_query = f"""SELECT * FROM asclist_asclist WHERE brand_id='{id_brands}';"""
        config.cursor.execute(asclist_select_query)
        asclist_records = config.cursor.fetchall()
        print(f'найдено {len(asclist_records)} запись(и): {asclist_records}')

        # Вывод списка из найденных АСЦ
        for asc in range(len(asclist_records)):
            list_id = asclist_records[asc][1]
            asc_select_query = f"""SELECT * FROM asclist_asc WHERE id='{list_id}';"""
            config.cursor.execute(asc_select_query)
            asc_records = config.cursor.fetchone()
            print(f'{asc_records}')

            cg_brand = asclist_records[asc][3]
            cg_brand_query = f"""SELECT * FROM asclist_commoditygroup WHERE id='{cg_brand}';"""
            config.cursor.execute(cg_brand_query)
            cg_brand_records = config.cursor.fetchone()
            print(f'{cg_brand_records}')
            if flag_cd_brand:
                await message.answer(
                    f'По данному бренду предусмотрена курьерская отправка!\n\n'
                    f'📱 Группа товаров: {cg_brand_records[1]}\n'
                    f'💼 Название АСЦ: {asc_records[1]}\n'
                    f'🏢 Город: {asc_records[4]}\n'
                    f'📩 Эл.почта: {asc_records[5]}\n'
                )
            else:
                await message.answer(
                    f'📱 Группа товаров: {cg_brand_records[1]}\n'
                    f'💼 Название АСЦ: {asc_records[1]}\n'
                    f'🏢 Адрес: {asc_records[3]}\n'
                    f'📞 Номер телефона: {asc_records[2]}\n'
                )

    except Exception as _ex:
        print('Не удалось прочитать данные из таблицы')
        await message.answer(
            f'По бренду "{brand_keys}" - записей не найдено'
        )
    finally:
        if config.sql_connection:
            print('Соединение с БД закрыто')


async def main():
    await config.dp.start_polling(config.bot)

if __name__ == '__main__':
    asyncio.run(main())

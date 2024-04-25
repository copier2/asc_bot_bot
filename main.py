import asyncio

from aiogram import F
from aiogram.types import Message

from config import config


@config.DP.message(F.text == '/start')
async def cmd_start(message: Message):
    """Стартовое сообщение при вызове команды /start"""
    await message.answer(
        f'Привет {message.from_user.first_name}, я твой виртуальный помощник'
    )


@config.DP.message(F.text == '/about')
async def cmd_about(message: Message):
    await message.answer(
        f'<b>Бот для поиска АСЦ по бренду</b>\n\n'
        f'<i>Предназначен исключительно для использования сотрудниками М-Видео/Эльдорадо</i>\n\n'
        f'БД содержит:\n'
        f'<b>{config.BRAND_COUNT_RECORDS}</b> бренд(ов)\n'
        f'{config.ASC_COUNT_RECORDS} наименований АСЦ: \n\n'
        f'Последнее обновление БД по АСЦ: <b>{config.UPDATE_DATE_BD}</b>\n'
        f'Текущая версия бота: <b>{config.BOT_VERSION}</b>\n',
        parse_mode='HTML'
    )


@config.DP.message()
async def get_text_bd(message: Message):
    brand_keys = message.text
    try:
        # Поиск id бренда по введенному запросу
        brand_select_query = f"""SELECT * FROM asclist_brand WHERE title='{brand_keys}';"""
        config.CURSOR.execute(brand_select_query)
        brand_records = config.CURSOR.fetchone()
        id_brands = brand_records[0]
        flag_cd_brand = brand_records[2]
        print(f'Для запроса "{brand_keys}" с id "{id_brands}:"')

        # Поиск записей в списке АСЦ по id бренда
        asclist_select_query = f"""SELECT * FROM asclist_asclist WHERE brand_id='{id_brands}';"""
        config.CURSOR.execute(asclist_select_query)
        asclist_records = config.CURSOR.fetchall()
        print(f'найдено {len(asclist_records)} запись(и): {asclist_records}')

        # Вывод списка из найденных АСЦ
        for asc in range(len(asclist_records)):
            list_id = asclist_records[asc][1]
            asc_select_query = f"""SELECT * FROM asclist_asc WHERE id='{list_id}';"""
            config.CURSOR.execute(asc_select_query)
            asc_records = config.CURSOR.fetchone()
            print(f'{asc_records}')

            cg_brand = asclist_records[asc][3]
            cg_brand_query = f"""SELECT * FROM asclist_commoditygroup WHERE id='{cg_brand}';"""
            config.CURSOR.execute(cg_brand_query)
            cg_brand_records = config.CURSOR.fetchone()
            print(f'{cg_brand_records}')
            if flag_cd_brand:
                await message.answer(
                    f'<b>{asc_records[1]}</b>\n\n'
                    f'<i>По данному бренду предусмотрена курьерская отправка!</i>\n\n'
                    f'Группа товаров: {cg_brand_records[1]}\n\n'
                    f'🏢 Адрес: {asc_records[3]}\n'
                    f'☎️ Телефон: {asc_records[2]}\n'
                    f'📨 E-mail: {asc_records[5]}\n'
                    f'🖥 Сайт: {asc_records[6]}\n',
                    parse_mode='HTML'
                )
            else:
                await message.answer(
                    f'<b>{asc_records[1]}</b>\n\n'
                    f'Группа товаров: {cg_brand_records[1]}\n\n'
                    f'🏢 Адрес: {asc_records[3]}\n'
                    f'☎️ Телефон: {asc_records[2]}\n'
                    f'📨 E-mail: {asc_records[5]}\n'
                    f'🖥 Сайт: {asc_records[6]}\n',
                    parse_mode='HTML'
                )

    except Exception as _ex:
        print('Не удалось прочитать данные из таблицы')
        await message.answer(
            f'По бренду "{brand_keys}" - записей не найдено'
        )
    finally:
        if config.SQL_CONNECTION:
            print('Соединение с БД закрыто')


async def main():
    await config.DP.start_polling(config.BOT)

if __name__ == '__main__':
    asyncio.run(main())

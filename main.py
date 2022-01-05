import json
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

from link_parser import collect_links

bot = Bot(token="5007015200:AAEbpSuOiHOvx-kYl5PRvK2V7d3d14Nqi04",
          parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Начинай :)")


@dp.message_handler(Text(equals="KmxKR7A2"))
async def get_streamers(message: types.Message):
    await message.answer("Ожидайте :)")
    collect_links()

    with open("result.json", encoding="utf-8") as file:
        data = json.load(file)

    for index, item in enumerate(data):
        streamer_info = f'{hlink(item["streamer"], item["link"])}\n' \
                        f'{hbold("Зрителей ")}{item["count_of_viewers"]}\n{item["steam_trade_link"]}\n{item["steam_link"]}\n{item["steam_personal_link"]}\n{item["Command available"]}'
        if index % 10 == 0:
            time.sleep(5)
            print("Отправлено 10 сообщений")
        await message.answer(streamer_info)


def main():
    print("Started")
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

from aiogram import Bot, Dispatcher, executor, types
import telebot
import requests
import json
import datetime
import asyncio

token = '5364518161:AAGm_JkM-h6LFBb4ZOKaxt0StrabQE6RmxU'

weather_api_key = 'a20597ec83b5f2e21e30e41f03be89f9'

qstn = dict()

bot = Bot(token)

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def hello_message(message):
    await message.answer(message.chat.id, "шалом, православные")


@dp.message_handler(commands=['help'])
async def help_message(message):
    await message.answer('помоги себе сам\n Я умею узнавать погоду, администрировать чат \n Если взаимодействие требует запроса, нужно вызывать команду реплаем на сообщение с запросом')

@dp.message_handler(commands=['get_out'])
async def get_out_message(message):
    await message.answer("пока")
    await bot.leave_chat(message.chat.id)

@dp.message_handler(commands=['make_admin'])
async def make_admin_message(message):
    if not message.reply_to_message:
        return await message.answer('Нужно отправить эту команду в ответ на сообщение пользователя, которого хотим сделать админом')
    await bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_change_info=True,
                                  can_delete_messages=True, can_invite_users=True, can_restrict_members=True,
                                  can_pin_messages=True, can_promote_members=True)
    await message.answer("шалом новому админу")

@dp.message_handler(commands=['ban'])
async def ban_message(message):
    if not message.reply_to_message:
        return await message.answer('Нужно отправить эту команду в ответ на сообщение пользователя, которого хотим забанить')
    await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.answer("забанен")


@dp.message_handler(commands=['unban'])
async def unban_message(message):
    if not message.reply_to_message:
        return await message.answer('Нужно отправить эту команду в ответ на сообщение пользователя, которого хотим разбанить')
    await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.answer("разбанен")

@dp.message_handler(commands=['stats'])
async def stats_message(message):
    await message.answer("всего пользователей: " + str(await bot.get_chat_members_count(message.chat.id)))
    await message.answer("всего админов: " + str(len(await bot.get_chat_administrators(message.chat.id))))


@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message):
    res = await message.answer("Шалом, " + message.new_chat_members[0].first_name + "!\n Сколько раз фраза Around the world была употреблена в треке Daft Punk - Around the world?")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("1", callback_data="1"))
    markup.add(types.InlineKeyboardButton("200", callback_data="2"))
    markup.add(types.InlineKeyboardButton("144", callback_data="3"))
    markup.add(types.InlineKeyboardButton("42", callback_data="4"))
    await bot.send_message(message.chat.id, "Выбери правильный ответ", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data)
async def inline(c):
    if c.data == "3":
        await bot.send_message(c.message.chat.id, "Верно!")
    else:
        await bot.send_message(c.message.chat.id, "Неверно!")


@dp.message_handler(commands=['set_photo'])
async def set_photo_message(message):
    if not message.reply_to_message:
        return await message.answer('Нужно отправить эту команду в ответ на сообщение в котором будет фото чата')
    await bot.set_chat_photo(message.chat.id, bot.get_file_url(message.reply_to_message.text))


@dp.message_handler(commands=['set_title'])
async def set_title_message(message):
    if not message.reply_to_message:
        return await message.answer('Нужно отправить эту команду в ответ на сообщение в котором будет название чата')
    await bot.set_chat_title(message.chat.id, message.reply_to_message.text)

@dp.message_handler(commands=['get_weather'])
async def get_weather(message):
    if not message.reply_to_message:
        return await message.answer('Нужно отправить эту команду в ответ на сообщение в котором будет название города')

    res = json.loads(requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + message.reply_to_message.text + "&appid=" + weather_api_key + "&units=metric").text)

    if 'weather' not in res:
        return await message.answer('Город не найден')

    response = 'Погода:' + res['weather'][0]['description'] + '\n' + 'Температура:' + str(res['main']['temp']) + '\n' + 'Влажность:' + str(res['main']['humidity']) + '%' + '\n' + 'Давление:' + str(res['main']['pressure']) + 'кПА \n' + 'Скорость ветра:' + str(res['wind']['speed']) + 'м/с \n'
    if 'rain' in res:
        response += 'Осадки(мм за последний час):' + str(res['rain']['1h'])
    if 'snow' in res:
        response += 'Снег(мм за последний час):' + str(res['snow']['1h'])
    if 'clouds' in res:
        response += 'Облачность:' + str(res['clouds']['all']) + '%' + '\n'
    if 'sys' in res:
        response += 'Восход по Гринвичу: ' + datetime.datetime.fromtimestamp(res['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S') + '\n' + 'Закат по Гринвичу:' + datetime.datetime.fromtimestamp(res['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
    await message.answer(response)

@dp.message_handler(content_types='text')
async def message_reply(message):
    if "Артём" in message.text or "артём" in message.text or "Артем" in message.text or "артем" in message.text:
        await message.answer("дуралей")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
#bot.polling(none_stop=True, interval=0)

# -*- coding: utf-8 -*-

import asyncio
from InstagramAPI import InstagramAPI
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'bot_token'
LOGIN = 'instagram_login'
PASSW = 'instagram_password'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


async def Info(m):

    _id = m.from_user.id

    if isEnglish(m.text) is False:
        await bot.send_message(_id, 'Non English charset found')
        return
    elif 'http' in m.text:
        await bot.send_message(_id, 'Bad input')
        return

    insta = InstagramAPI(LOGIN, PASSW)
    status = insta.login()

    if status:
        _get_user = insta.searchUsername(m.text)

        if _get_user:
            dump = insta.LastJson['user']
            closed = True if dump['account_type'] == 1 else False

            if dump['is_private']:
                await bot.send_message(_id, 'This is closed account 🔒')
                return

            text = '💁🏼‍Name: ' + dump['full_name'] \
                + ' (' + dump['username'] + ')'

            text += ' ☑️\n' if dump['is_verified'] else '\n'
            email = 'None' if closed else dump['public_email']
            phone = 'None' if closed else dump['contact_phone_number']
            _zip = 'None' if closed else dump['zip']
            category = 'None' if closed else dump['category']

            text += '✉️E-Mail: ' + email + '\n' + \
                '📱Phone number: ' + phone + '\n' + \
                '📌ZIP: ' + _zip + '\n------\n' + \
                '🔖Category: ' + category + '\n------\n' + \
                '📝Bio: ' + dump['biography'] + '\n' + \
                'Followers: ' + str(dump['follower_count']) + '\n' + \
                'Following: ' + str(dump['following_count']) + '\n' + \
                'Post`s: ' + str(dump['media_count'])

            await bot.send_message(_id, text)

        else:
            await bot.send_message(_id, 'Check login 👈🏼')
    else:
        await bot.send_message(_id, 'Troubleshoot with bot account...')


@dp.message_handler()
async def check_language(message: types.Message):
    await Info(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

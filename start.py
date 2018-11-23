# -*- coding: utf-8 -*-

import telebot
from telebot.types import ForceReply
from InstagramAPI import InstagramAPI

bot = telebot.TeleBot("BOT_TOKEN")


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def Info(m):

    if isEnglish(m.text) is False:
        bot.send_message(m.chat.id, 'Non English charset found')
        return ''

    if 'http' in m.text:
        bot.send_message(m.chat.id, 'Bad input')
        return ''

    insta = InstagramAPI('login', 'password')
    status = insta.login()

    if status:
        _get_user = insta.searchUsername(m.text)

        if _get_user:
            dump = insta.LastJson['user']
            closed = True if dump['account_type'] == 1 else False

            if dump['is_private']:
                bot.send_message(m.chat.id, 'This is closed account 🔒')
                return ''

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

            bot.send_message(m.chat.id, text)

        else:
            bot.send_message(m.chat.id, 'Check login 👈🏼')
    else:
        bot.send_message(m.chat.id, 'Troubleshoot with bot account...')


@bot.message_handler(commands=['start'])
def on_start(m):
    bot.send_message(m.chat.id, "Hello. Send Instagram username to me.")


@bot.message_handler()
def main(message):
    Info(message)


def run():
    try:
        bot.polling(none_stop=True)
    except:
        run()


if __name__ == "__main__":
    run()

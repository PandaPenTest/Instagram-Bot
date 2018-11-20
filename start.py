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

    if isEnglish(m.text) == False:
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
            
            if dump['is_private']:
                bot.send_message(m.chat.id, 'This is closed account 🔒')
                return ''
            
            text = '💁🏼‍Name: ' + dump['full_name'] + ' (' + dump['username'] + ')'

            if dump['is_verified']:
                text += ' ☑️\n' 
            else:
                text += '\n'
            
            if dump['account_type'] == 1:
                text += '✉️E-Mail: None \n' + \
                    '📱Phone number: None\n' + \
                    '📌ZIP: None\n' + \
                    '🔖Category: None\n------\n'
            else:
                text += '✉️E-Mail: ' + dump['public_email'] + '\n' + \
                    '📱Phone number: ' + dump['contact_phone_number'] + '\n' + \
                    '📌ZIP: ' + dump['zip'] + '\n------\n' + \
                    '🔖Category: ' + dump['category'] + '\n------\n'
            
            text += '📝Bio: ' + dump['biography'] + '\n' + \
                    'Followers: ' + str(dump['follower_count']) + '\n' + \
                    'Following: ' + str(dump['following_count']) + '\n' + \
                    'Post`s: ' + str(dump['media_count'])
            
            bot.send_message(m.chat.id, text)

        else:
            bot.send_message(m.chat.id, 'Check login 👈🏼')
    else:
        bot.send_message(m.chat.id, 'Trubleshoot with bot account, maybe ☠️...')

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

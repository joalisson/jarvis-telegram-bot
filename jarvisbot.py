#!/usr/bin/env python
# encoding: utf-8

import logging
import urllib
import telegram

from textblob import TextBlob
from telegram import Updater
from telegram.dispatcher import run_async
from config import TOKEN


bot = telegram.Bot(TOKEN) 
updater = Updater(TOKEN, workers=10)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    text = unicode('Olá, eu sou o Jarvis! Um BOT com inteligência artificial, pronto para obedecer a seus comandos! Digite:'+'\n'\
        + '/search texto >> Para realizar buscas no Google'+'\n'\
        + '/fb texto >> Para realizar buscas no Facebook'+ '\n'\
        + '/en texto >> Para traduzir texto para Inglês.'+ '\n'\
        + '/help >> Caso precise de ajuda', 'utf-8')

    bot.sendMessage(update.message.chat_id, text=text)


def help(bot, update):
    text = unicode('Olá,'+ update.message.from_user.first_name +'. Você digitou /help. Este é o menu de ajuda. Escolha uma das opções:'+'\n'\
        + '/search texto >> Para realizar buscas no Google'+'\n'\
        + '/fb texto >> Para realizar buscas no Facebook'+ '\n'\
        + '/en texto >> Para traduzir texto para Inglês.', 'utf-8')

    bot.sendMessage(update.message.chat_id, text=text)


def search(bot, update, args):
    chat_id = update.message.chat_id
    term = text_replace(update.message.text)

    bot.sendMessage(chat_id, text=u'https://www.google.com.br/#q=%s' % term)


def fb_search(bot, update, args):
    chat_id = update.message.chat_id
    term = text_replace(update.message.text)

    bot.sendMessage(chat_id, text=u'https://www.facebook.com/search/top/?init=quick&q=%s' % term)


def jarvis(text):
    url = 'http://www.ed.conpet.gov.br/mod_perl/bot_gateway.cgi?server=0.0.0.0%3A8085&charset_post=utf-8&charset=utf-8&pure=1&js=0&tst=1&msg=' + text.encode('utf-8')
    data = urllib.urlopen(url).read()
    
    return data.strip()


def text_replace(text):
    text = u'%s' % text

    if '/en' in text:
        new_text = text.replace('/en', '')
    if '/br' in text:
        new_text = text.replace('/br', '')
    elif '/fb' in text:
        new_text = text.replace(' ', '+').replace('/fb', '')
    elif '/go' in text:
        new_text = text.replace(' ', '+').replace('/go', '')

    return new_text


def translate_en(bot, update):
    text = text_replace(update.message.text)
 
    chat_id = update.message.chat_id

    en_blob = TextBlob(text)
    en_text = en_blob.translate(to='en')

    return bot.sendMessage(chat_id, text=u'Tradução: %s' % str(en_text))


def translate_pt(bot, update):
    text = text_replace(update.message.text)
 
    chat_id = update.message.chat_id

    en_blob = TextBlob(text)
    pt_text = en_blob.translate(to='pt-BR')

    return bot.sendMessage(chat_id, text=u'Tradução: %s' % unicode(pt_text))


def message(bot, update):

    text = update.message.text
    chat_id = update.message.chat.id

    botgood = jarvis(text)
    bot.sendMessage(chat_id=chat_id, text=botgood, parse_mode=telegram.ParseMode.HTML)


def main():
    
    global updater

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("go", search)
    dp.addTelegramCommandHandler("fb", fb_search)
    dp.addTelegramCommandHandler("en", translate_en)
    dp.addTelegramCommandHandler("br", translate_pt)
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("say", message)

    updater.start_polling()
    updater.idle()

    update_queue = updater.start_polling(poll_interval=0.1, timeout=10)

    while True:
        try:
            text = raw_input()
        except NameError:
            text = input()

        if text == 'stop':
            updater.stop()
            break

        elif len(text) > 0:
            update_queue.put(text)


if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
import info 
import welcome
import bredis
import yaml
import superadmin

#Config

#Bot Configuration
with open("config.yml", 'r') as configfile:
    cfg = yaml.load(configfile)

for section in cfg:
    TOKEN = str(cfg['apitoken'])
    log = str(cfg['log'])
    creator = int(cfg['creator-id'])


# Enable logging
logging.basicConfig(format= u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(log)
formatter = logging.Formatter(u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

logger = logging.getLogger(__name__)


class WelcomeFilter(BaseFilter):
        def filter(self, message):
            return bool(message.new_chat_member)
welcome_filter = WelcomeFilter()

def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def test(bot, update, args):
    update.message.reply_text('Test failed. Try again mf')

def add(bot, update):
    fr = update.message.from_user
    bredis.adduser(fr.id, fr.first_name, fr.last_name, fr.username)
    c = update.message.chat
    if update.message.chat.type != 'private':
        bredis.addgroup(c.id, c.title, c.username)
    else:
        return None

def get(bot, update, args):
    update.message.reply_text(bredis.user.all(update.message.from_user.id))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("u", info.info_user))
    dp.add_handler(CommandHandler("test", test, pass_args=True))
    dp.add_handler(CommandHandler("setwelc", welcome.set, pass_args=True))
    dp.add_handler(CommandHandler("getwelc", welcome.get, pass_args=True))
    dp.add_handler(CommandHandler("groupwelc", welcome.groupset, pass_args=True))
    dp.add_handler(CommandHandler("addadmin", superadmin.add, pass_args=True))
    dp.add_handler(CommandHandler("bsend", superadmin.send, pass_args=True))
    dp.add_handler(CommandHandler("delwelc", welcome.rem, pass_args=True))
    dp.add_handler(CommandHandler("getu", get, pass_args=True))









    # non commands
    dp.add_handler(MessageHandler(welcome_filter, welcome.msg))
    dp.add_handler(MessageHandler(Filters.text, add))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
import info 
import welcome
import bredis

#Config
TOKEN = "190871990:AAGkxombmZIPIWSWPEGePfBER0TnQ_rQf70"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

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

def test(bot, update):
    #update.message.reply_text('Test failed. Try again mf')
    test = bredis.exists(update.message.chat.id) #bredis.exists(update.message.from_user.id)

#    if test == 1:
#        update.message.reply_text(bredis.getwelc(update.message.from_user.id), quote=False)
#    else:
#        return True
    erm = str(update.message.chat.type)
    update.message.reply_text(erm, quote=False)
def add(bot, update):
    fr = update.message.from_user
    bredis.adduser(fr.id, fr.first_name, fr.last_name, fr.username)
    c = update.message.chat
    if update.message.chat.type != 'private':
        bredis.addgroup(c.id, c.title, c.username)
    else:
        return None

def getwelc(bot, update, args):
    if update.message.from_user.id == 81772130:
        uid = int(args[0])
        welc = bredis.getwelc(uid)
        msg = "This is `{0}`'s welcome message:\n{1}".format(uid, welc)
        update.message.reply_text(msg, quote=False, parse_mode='Markdown')
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("u", info.info_user))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("setwelc", welcome.set, pass_args=True))
    dp.add_handler(CommandHandler("getwelc", getwelc, pass_args=True))






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

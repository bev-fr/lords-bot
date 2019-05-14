#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, InlineQueryHandler
import logging
import utils
import welcome
import bredis
import yaml
import superadmin

#Config
from config import token, log, creator


# Enable logging
logging.basicConfig(format= u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(log)
formatter = logging.Formatter(u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

logger = logging.getLogger(__name__)


#class WelcomeFilter(BaseFilter):
#        def filter(self, message):
#            if message.new_chat_member:
#                return True
#            else:
#                return False
#welcome_filter = WelcomeFilter()


def start(bot, update):
    update.message.reply_text('Hello, I am lil cat lord, a bot that wecomes users to groups. Use /help to learn about all my commands')


def helpm(bot, update):
    resp = "User Commands:\n/u - Get info about the user \n\nGroup Admin Commands:\n/groupwelc - allows you to set the welcome message for the group. \n\nYou can use these variables to add info about the user into the welcome message:\n{uid} - the user's ID\n{fanme} - the user's first name\n{lname} - the user's last name\n{username} - the user's username \n\nCustom Welcomes: \nUse /mywelc to set your custom welcome. You can also reply to a gif to add it to your welcome. Example: t.me/benthe/7"
    if update.message.chat.id > 0:
        update.message.reply_text(resp, disable_web_page_preview=True)
    else:
        try:
            bot.sendMessage(update.message.from_user.id, resp, disable_web_page_preview=True)
        except Unauthorized:
            update.message.reply_text("Please PM me first ~")

        update.message.reply_text("I have sent you a PM")

def hug(bot, update, args):
    msg = []
    try:
        hugNumber = int(args[0])
        if hugNumber == int(69):
            for x in range(hugNumber):
                    msg.append("😏")
        elif hugNumber < 99:
            for x in range(hugNumber):
                    msg.append("*hug*")
        else:
            msg.append("Too many, hugs rejected")
    except ValueError:
        msg.append("Insert how many hugs you want by typing : /hug <number>")
    replyMessage = update.message.reply_to_message
    if replyMessage is not None:
        message = update.message 
        bot.sendMessage(message.chat.id, " ".join(msg), reply_to_message_id = replyMessage.message_id)
    else:
        update.message.reply_text(" ".join(msg), quote=False)


def stab(bot, update):
    if update.message.from_user.id in creator:
        msg = "*stab stab stabs {1}*"
    else:
        if update.message.reply_to_message.from_user.id in creator:
            msg = "nooooooooo! *takes knife and stab stab stabs {0}*"
        else:
            msg = "*cautiously hands knife to {0} 🙈🙈🙈*"
    update.message.reply_text(msg.format(update.message.from_user.first_name, update.message.reply_to_message.from_user.first_name))


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def logGroupIds(bot ,update):
    if update.message.chat.id < 0:
        bredis.groupList.add(update.message.chat.id)

def grouplist(bot, update):
    raw_groups = bredis.groupList.get()
    groups = []
    for i in raw_groups:
        groups.append(str(i))
    resp = "I have seen {num} groups!"
    update.message.reply_text(
            resp.format(
                num=len(groups)),
            quote=False,
            parse_mode='Markdown')



def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    ###Commands
    #all users
    dp.add_handler(CommandHandler("u", utils.info, pass_args=True))
    dp.add_handler(CommandHandler("test", welcome.msg))
    dp.add_handler(CommandHandler("start@benthebot", start))
    dp.add_handler(CommandHandler("help", helpm))
    dp.add_handler(CommandHandler("hug", hug, pass_args=True))
    dp.add_handler(CommandHandler("stab", stab))
    dp.add_handler(CommandHandler("redis", utils.redis_info, pass_args=True))
    dp.add_handler(CommandHandler("mywelc", welcome.set_welc_self, pass_args=True))
    dp.add_handler(CommandHandler("groups", grouplist))


    #superadmin only
    dp.add_handler(CommandHandler("setwelc", welcome.set_welc_other, pass_args=True))
    dp.add_handler(CommandHandler("getwelc", welcome.get, pass_args=True))
    dp.add_handler(CommandHandler("delwelc", welcome.rem, pass_args=True))
    dp.add_handler(CommandHandler("block", superadmin.block_user, pass_args=True))
    dp.add_handler(CommandHandler("unblock", superadmin.unblock_user, pass_args=True))
    dp.add_handler(CommandHandler("blocked", superadmin.list_blocked_users))


    #groupadmin only
    dp.add_handler(CommandHandler("groupwelc", welcome.groupset, pass_args=True))

    #creator only
    dp.add_handler(CommandHandler("trust", superadmin.add, pass_args=True))
    dp.add_handler(CommandHandler("bsend", superadmin.send, pass_args=True))
    dp.add_handler(CommandHandler("adminsend", superadmin.adminsend, pass_args=True))
    dp.add_handler(CommandHandler("listadmins", superadmin.list_admins, pass_args=True))
    
    # non commands
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome.msg))
    dp.add_handler(MessageHandler(Filters.text, logGroupIds))

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

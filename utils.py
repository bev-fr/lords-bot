import telegram as tg
import telegram.ext as tg_ext
import re
import datetime
import psutil


def info_meta(bot, update, args):
    commands = {
    	'user': info_user,
    	'chat': info_chat,
    	'message': info_message,
    	'full' : info_full
    }
    if args[0] in commands:
    	commands[args[0]](bot, update)


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def info(bot, update):
    user = update.message.reply_to_message.from_user
    timestamp = update.message.reply_to_message.date
    resp = []
    resp = addUserToResp(user, resp)
    resp.append('At {} UTC'.format(str(timestamp)))
    if update.message.reply_to_message.forward_from:
        resp.append('\nForwarded From:')
        addUserToResp(update.message.reply_to_message.forward_from, resp)
        forwardTimestamp = update.message.reply_to_message.forward_date
        resp.append('Originally sent at {} UTC'.format(forwardTimestamp))
    #if update.message.reply_to_message.forward_from_chat:
        #chan = update.message.reply_to_message.forward_from_chat
    resp = '\n'.join(resp)
    bot.send_message(update.message.chat_id, resp, parse_mode='Markdown')


def addUserToResp(user, resp):
    if user.username:
        resp.append(escape_markdown('@{}'.format(user.username)))
        resp.append('`{}`'.format(user.id))
        resp.append(escape_markdown('First: {}'.format(user.first_name)))
    if user.last_name:
    	resp.append(escape_markdown('Last: {}'.format(user.last_name)))
    return resp

def ping(bot, update):
    msgSent = update.message.date
    msgRecieved = datetime.datetime.now()
    pingTime = msgSent - msgRecieved 
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    resp = "Time to receive ping message: `{time}` \nCurrent CPU usage: `{cpu}%` \nCurrent RAM usage: `{ram}%`"
    resp = resp.format(time=pingTime, cpu=cpu, ram=ram)
    update.message.reply_text(resp, quote=False, parse_mode='Markdown')

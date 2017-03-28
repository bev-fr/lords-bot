import telegram as tg
import telegram.ext as tg_ext
import re
import datetime
import psutil
from subprocess import call
from background import background




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

def sys_info(bot, update):
    msgSent = update.message.date
    msgRecieved = datetime.datetime.now()
    pingTime = msgRecieved - msgSent 
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    resp = "Time to receive message: `{time}` \nCurrent CPU usage: `{cpu}%` \nCurrent RAM usage: `{ram}%`"
    resp = resp.format(time=pingTime, cpu=cpu, ram=ram)
    update.message.reply_text(resp, quote=False, parse_mode='Markdown')

@background
def kahoot_rand(bot, update, args):
    gid = args[0]
    nick = args[1]
    num = args[2]
    call(["./kahoot-rand", gid, nick, num])
    resp="{num} bots started with the name \"{nick}\" on `{gid}`"
    update.message.reply_text(resp.format(num=num, nick=nick, gid=gid), parse_mode='Markdown')

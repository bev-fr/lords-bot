import bredis
import re
import utils
from config import creator

###Creator Only
def send(bot, update, args):
    if creator == update.message.from_user.id:
        gid = args[0]
        del args[0]
        msg = utils.escape_markdown(' '.join(args))
        bot.sendMessage(gid, msg)# parse_mode='Markdown')
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

def add(bot, update, args):
    if creator == update.message.from_user.id:
        bredis.superadmin.add(args)
        msg = "*shyly peeks out from behind lord* hi {name} youre no longer a stranger"
        #name = bredis.
        update.message.reply_text(msg.format(name=bredis.user.name(args[0])), quote=False)
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

def adminsend(bot, update, args):
    if creator == update.message.from_user.id:
        for uid in bredis.superadmin.get():
            bot.sendMessage(uid, ' '.join(args).format(u=update.message.from_user.id))
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

###SuperAdmin Only
def block_user(bot, update, args):
    adminId = update.message.from_user.id
    isAdmin = bredis.superadmin.check(adminId)
    if isAdmin is True:
        blockedId = args[0]
        bredis.blocked.add(str(blockedId))
        update.message.reply_text('`{}` has been blocked from setting their own welcome'.format(blockedId), quote=False, parse_mode='Markdown')

def list_blocked_users(bot, update):
    adminId = update.message.from_user.id
    isAdmin = bredis.superadmin.check(adminId)
    if isAdmin is True:
        blockedUsers = bredis.blocked.get()
        resp = []
        for i  in blockedUsers:
            resp.append(str(i))
        update.message.reply_text('\n'.join(resp), quote=False, parse_mode='Markdown')

def unblock_user(bot, update, args):
    adminId = update.message.from_user.id
    isAdmin = bredis.superadmin.check(adminId)
    if isAdmin is True:
        blockedId = args[0]
        bredis.blocked.rem(str(blockedId))
        update.message.reply_text('`{}` has been unblocked'.format(blockedId), quote=False, parse_mode='Markdown')

import bredis
import utils
from config import creator

def creator_only(func):
    def isCreator(bot, update, args):
        if creator == update.message.from_user.id:
            func(bot, update, args)
        else:
            update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)
    return isCreator


###Creator Only
@creator_only
def send(bot, update, args):
    gid = args[0]
    del args[0]
    msg = utils.escape_markdown(' '.join(args))
    bot.sendMessage(gid, msg)# parse_mode='Markdown')

@creator_only
def add(bot, update, args):
    bredis.superadmin.add(args)
    msg = "*shyly peeks out from behind lord* hi {name} youre no longer a stranger"
    #name = bredis.
    update.message.reply_text(msg.format(name=bredis.user.name(args[0])), quote=False)

@creator_only
def adminsend(bot, update, args):
    for uid in bredis.superadmin.get():
        bot.sendMessage(uid, ' '.join(args).format(u=update.message.from_user.id))


def sAdmin_only(func):
    def isAdmin(bot, update, args):
        adminId = update.message.from_user.id
        isAdmin = bredis.superadmin.check(adminId)
        if isAdmin is True:
            func(bot, update, args)
        else:
            return None
    return isCreator


###SuperAdmin Only
def block_user(bot, update, args):
    blockedId = args[0]
    bredis.blocked.add(str(blockedId))
    update.message.reply_text('`{}` has been blocked from setting their own welcome'.format(blockedId), quote=False, parse_mode='Markdown')

def list_blocked_users(bot, update):
    blockedUsers = bredis.blocked.get()
    resp = []
    for i  in blockedUsers:
        resp.append(str(i))
    update.message.reply_text('\n'.join(resp), quote=False, parse_mode='Markdown')

def unblock_user(bot, update, args):
    blockedId = args[0]
    bredis.blocked.rem(str(blockedId))
    update.message.reply_text('`{}` has been unblocked'.format(blockedId), quote=False, parse_mode='Markdown')

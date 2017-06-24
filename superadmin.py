import bredis
import utils
from config import creator


def creator_only(func):
    def isCreator(bot, update, *args, **kwargs):
        if update.message.from_user.id in creator:
            func(bot, update, *args, **kwargs)
        else:
            update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)
    return isCreator

###Creator Only
@creator_only
def add(bot, update, args):
    bredis.superadmin.add(args)
    chat_id = update.message.chat.id
    user_id = args[0]
    try:
        member = bot.get_chat_member(chat_id, user_id)
        name = member.user.first_name
        msg = "*shyly peeks out from behind lord* hi {} youre no longer a stranger"
    except:
        name = args[0]
        msg = "{} is now a superadmin"
    update.message.reply_text(msg.format(name), quote=False)

@creator_only
def adminsend(bot, update, args):
    for uid in bredis.superadmin.get():
        bot.sendMessage(uid, ' '.join(args).format(u=update.message.from_user.id))


def sAdmin_only(func):
    def isAdmin(bot, update, *args, **kwargs):
        adminId = update.message.from_user.id
        isAdmin = bredis.superadmin.check(adminId)
        args = []
        if isAdmin is True:
            func(bot, update, *args, **kwargs)
        else:
            update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)
    return isAdmin


###SuperAdmin Only
@sAdmin_only
def block_user(bot, update, args):
    blockedId = args[0]
    bredis.blocked.add(str(blockedId))
    update.message.reply_text('`{}` has been blocked from setting their own welcome'.format(blockedId), quote=False, parse_mode='Markdown')

@sAdmin_only
def list_blocked_users(bot, update):
    blockedUsers = bredis.blocked.get()
    resp = []
    for i  in blockedUsers:
        resp.append(str(i))
    update.message.reply_text('\n'.join(resp), quote=False, parse_mode='Markdown')

@sAdmin_only
def unblock_user(bot, update, args):
    blockedId = args[0]
    bredis.blocked.rem(str(blockedId))
    update.message.reply_text('`{}` has been unblocked'.format(blockedId), quote=False, parse_mode='Markdown')

@sAdmin_only
def send(bot, update, args):
    gid = args[0]
    del args[0]
    msg = utils.escape_markdown(' '.join(args))
    bot.sendMessage(gid, msg)# parse_mode='Markdown')


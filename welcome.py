import bredis
from mwt import MWT
from config import log_channel
from superadmin import sAdmin_only


#This is /mywelc
def set_welc_self(bot, update, args):
    uid = update.message.from_user.id
    isBlocked = bredis.blocked.check(uid) 
    if isBlocked is True:
        return None
    elif args == []:
        welc = bredis.getwelc(uid)
        if welc != None:
            resp = "Your current welcome message is:\n{}"
        else:
            resp = "You do not currently have a welcome message, please PM me to set one"
        update.message.reply_text(resp.format(welc), quote=False, parse_mode='Markdown')
    else:
        welc_msg = args
        set_welc(bot, update, uid, welc_msg)
        resp = "Your welcome message was set to:\n{}" 
        update.message.reply_text(resp.format(bredis.getwelc(uid)), quote=False, parse_mode='Markdown')


#This is /setwelc
@sAdmin_only
def set_welc_other(bot, update, args):
    uid = args[0]
    del args[0]
    welc_msg = args
    set_welc(bot, update, uid, welc_msg)
    msg = "`{0}`'s welcome message set to:\n{1}" 
    update.message.reply_text(msg.format(uid, bredis.getwelc(uid)), quote=False, parse_mode='Markdown')


def set_welc(bot, update, uid, message):
    user = update.message.from_user
    welc_msg = ' '.join(message)
    chatid = update.message.chat.id
    bredis.welcome.set(welc_msg, uid)
    if update.message.reply_to_message:
        if update.message.reply_to_message.document:
            file_id = update.message.reply_to_message.document.file_id
            bredis.welcome.file_id.set(file_id, uid)
            bredis.welcome.type.set('gif', uid)
            if user.id == uid:
                log_msg = "{fname} {lname} ({uid}) (@{username}) has set their welcome message to:\n {welc} \nIn {chatid}"
            else: 
                log_msg = "{fname} {lname} ({setter_id}) (@{username}) has set {uid}'s welcome message to:\n {welc} \nIn {chatid}"
            bot.sendDocument(
                    log_channel,
                    file_id,
                    caption=log_msg.format(
                        fname=user.first_name,
                        lname=user.last_name,
                        setter_id=user.id,
                        uid=uid,
                        username=user.username,
                        welc=welc_msg,
                        chatid=chatidi
                        )
                    )
    else:
        bredis.welcome.type.set('text', uid)
        if user.id == uid:
            log_msg = "{fname} {lname} (`{uid}`) (@{username}) has set their welcome message to:\n {welc} \nIn {chatid}"
        else: 
            log_msg = "{fname} {lname} (`{setter_id}`) (@{username}) has set `{uid}`'s welcome message to:\n {welc} \nIn {chatid}"
        bot.sendMessage(
                log_channel,
                log_msg.format(
                    fname=user.first_name,
                    lname=user.last_name,
                    setter_id=user.id,
                    uid=uid,
                    username=user.username,
                    welc=welc_msg,
                    chatid=chatid
                    ),
                parse_mode='Markdown'
                )


def groupset(bot, update, args):
    user = update.message.from_user
    gid = update.message.chat.id
    if update.message.from_user.id in get_admin_ids(bot, update.message.chat_id):
        bredis.welcome.set(' '.join(args), gid)
        if update.message.reply_to_message:
            if update.message.reply_to_message.document:
                file_id = update.message.reply_to_message.document.file_id
                bredis.welcome.file_id.set(file_id, gid)
                bredis.welcome.type.set('gif', gid)
        else:
            bredis.welcome.type.set('text', gid)
        msg = "Group welcome message set to:\n{0}" 
        update.message.reply_text(msg.format(bredis.getwelc(gid)), quote=False, parse_mode='HTML')
    else:
        update.message.reply_text('uhh...{0} i dont think youre an admin...'.format(update.message.from_user.first_name), quote=False, parse_mode='HTML')
        return None
        
@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
        """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
        return [admin.user.id for admin in bot.getChatAdministrators(chat_id)]


#Delete welcomes
@sAdmin_only
def rem(bot, update, args):
    uid = args[0]
    bredis.welcome.delete(uid)
    msg = "`{0}`'s welcome message deleted" 
    update.message.reply_text(msg.format(uid), quote=False, parse_mode='Markdown')


#Returns a users welcome
@sAdmin_only
def get(bot, update, args):
    if update.message.reply_to_message is not None:
        uid = update.message.reply_to_message.from_user.id
    else:
        uid = int(args[0])
    welc = bredis.getwelc(uid)
    msg = "This is `{0}`'s welcome message:\n{1}".format(uid, welc)
    update.message.reply_text(msg, quote=False, parse_mode='Markdown')


#Checks if a user has a welcome and sends it
def msg(bot, update):
    user = update.message.new_chat_member
    rawwelc = bredis.getwelc(user.id)
    uid = user.id
    welc = "{0} `({1})`".format(rawwelc, uid)
    exists = bredis.exists(user.id)
    msg_type = bredis.welcome.type.get(uid)
    file_id = bredis.welcome.file_id.get(uid)

    if rawwelc != None and exists == 1: 
        if msg_type == 'gif':
            welc = "{0} ({1})".format(rawwelc, uid)
            update.message.reply_document(quote=False,
                    disable_web_page_preview=True,
                    document=file_id,
                    caption=welc)
        else:
            welc = "{0} `({1})`".format(rawwelc, uid)
            update.message.reply_text(welc,
                    quote=False,
                    parse_mode='Markdown',
                    disable_web_page_preview=True)

    else:
        uid = update.message.chat.id
        if msg_type == 'gif':
            groupwelc = bredis.getwelc(update.message.chat.id).format(fname=user.first_name,
                lname=user.last_name,
                uid=user.id,
                username=user.username)
            if groupwelc != None:
                update.message.reply_document(document=file_id,
                        quote=False,
                        parse_mode='Markdown',
                        disable_web_page_preview=True,
                        caption=groupwelc)
            else:
                return None 
        else:
            groupwelc = bredis.getwelc(update.message.chat.id).format(fname=user.first_name,
                    lname=user.last_name,
                    uid=user.id,
                    username=user.username)
            if groupwelc != None:
                try:
                    update.message.reply_text(groupwelc,
                            quote=False,
                            parse_mode='Markdown',
                            disable_web_page_preview=True)
                except:
                    update.message.reply_text(groupwelc,
                            quote=False)
            else:
                return None 


import bredis


def send(bot, update, args):
    if 81772130 == update.message.from_user.id:
        gid = args[0]
        del args[0]
        bot.sendMessage(gid, ' '.join(args).format(u=update.message.from_user.id))
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)


def add(bot, update, args):
    if 81772130 == update.message.from_user.id:
        bredis.addsuperadmin(args)
        msg = "*shyly peeks out from behind lord* hi {name} youre no longer a stranger"
        #name = bredis.
        update.message.reply_text(msg.format(name=bredis.user.name(args[0])), quote=False)
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)


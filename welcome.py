import bredis

def set(bot, update, args):
    uid = update.message.from_user.id 
    isAdmin = bredis.isSuperSdmin()
    if isAdmin(uid) is True:
        uid = args[0]
        del args[0]
        print(args)
        print(uid)
        bredis.setwelc(' '.join(args), uid)
        msg = "`{0}`'s welcome message set to:\n{1}" 
        update.message.reply_text(msg.format(uid, bredis.getwelc(uid)), quote=False, parse_mode='Markdown')
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

#def load():
#    f = open('welc.yml')
#    welcs = yaml.safe_load(f)
#    f.close()
#    print (welcs)


def msg(bot, update):
    gwelc = {-1001062976534: ("Oh no, it's *", update.message.new_chat_member.first_name, "*! Everyone hide! We have ", str(update.message.new_chat_member.id), " nanoseconds to run!")}
    rawwelc = bredis.getwelc(update.message.new_chat_member.id)
    uid = update.message.new_chat_member.id
    welc = "{0} `({1})`".format(rawwelc, uid)

    qroupwelc = bredis.getwelc(update.message.chat.id)


    if rawwelc != None: #bredis.exists(update.message.new_chat_member.id) == 1:
        update.message.reply_text(welc, quote=False, parse_mode='Markdown')


    else: 
        if update.message.chat.id in gwelc:
            #bredis.exists(update.message.chat.id) == 1:
            update.message.reply_text(''.join(gwelc[update.message.chat.id]), quote=False, parse_mode='Markdown')

        else:
            return None #update.message.reply_text('Please contact @benthecat to set a welcome message for ur group, as he is way to lazy too make a way for you to do it', quote=False, parse_mode='Markdown')


import bredis

def set(bot, update, args):
    return None

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


    if bredis.exists(update.message.new_chat_member.id) == 1:
        update.message.reply_text(welc, quote=False, parse_mode='Markdown')


    else: 
        if update.message.chat.id in gwelc:
            #bredis.exists(update.message.chat.id) == 1:
            update.message.reply_text(''.join(gwelc[update.message.chat.id]), quote=False, parse_mode='Markdown')

        else:
            update.message.reply_text('Please contact @benthecat to set a welcome message for ur group, as he is way to lazy too make a way for you to do it', quote=False, parse_mode='Markdown')


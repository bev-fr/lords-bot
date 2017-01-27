import telegram as tg
import telegram.ext as tg_ext
import re


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


def info_user(bot, update):
	user = update.message.reply_to_message.from_user
	resp = []
	if user.username:
		resp.append(escape_markdown('@{}'.format(user.username)))
	resp.append('ID: `{}`'.format(user.id))
	resp.append(escape_markdown('First: {}'.format(user.first_name)))
	if user.last_name:
		resp.append(escape_markdown('Last: {}'.format(user.last_name)))
	resp = '\n'.join(resp)
	bot.send_message(update.message.chat_id, resp, parse_mode='Markdown')


def info_chat(bot, update):
	chat = update.message.chat
	resp = '{}:\n{}'.format(chat.title, chat.id)
	bot.send_message(update.message.chat_id, resp)


def info_message(bot, update):
	message = update.message.reply_to_message.message_id
	resp = message
	bot.send_message(update.message.chat_id, resp)


def info_full(bot, update):
	message = update.message.reply_to_message
	resp = 'I will print the message details.'
	bot.send_message(update.message.chat_id, resp)
	print(message)


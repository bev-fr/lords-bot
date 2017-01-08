#!/usr/bin/env python
import telegram as tg
import telegram.ext as tg_ext

def info_meta(bot, update, args):
	commands = {
		'user': info_user,
		'chat': info_chat,
		'message': info_message,
		'full' : info_full
	}
	if args[0] in commands:
		commands[args[0]](bot, update)

def info_user(bot, update):
	user = update.message.reply_to_message.from_user
	resp = []
	if user.username:
		resp.append('@{}'.format(user.username))
	resp.append('ID: <code>{}</code>'.format(user.id))
	resp.append('First: {}'.format(user.first_name))
	if user.last_name:
		resp.append('Last: {}'.format(user.last_name))
	resp = '\n'.join(resp)
	bot.send_message(update.message.chat_id, resp, parse_mode='HTML')

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

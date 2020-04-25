import config
import telebot
import cherrypy
from telebot import types
from chatbase import Message
from database import set_state, get_state
import sqlite3


# WEBHOOK
WEBHOOK_HOST = '0.0.0.0'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)


# bot logic
bot = telebot.TeleBot(config.token)


class WebhookServer(object):
	@cherrypy.expose
	def index(self):
		if 'content-length' in cherrypy.request.headers and \
				'content-type' in cherrypy.request.headers and \
				cherrypy.request.headers['content-type'] == 'application/json':
			length = int(cherrypy.request.headers['content-length'])
			json_string = cherrypy.request.body.read(length).decode("utf-8-")
			update = telebot.types.Update.de_json(json_string)
			bot.process_new_updates([update])
			return ''
		else:
			raise cherrypy.HTTPError(403)


# keyboard sales and promo
markup_MAIN = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
button_sales = telebot.types.KeyboardButton(config.SALES_BUTTON)
button_promo = telebot.types.KeyboardButton(config.PROMOCODES_BUTTON)
button_contact = telebot.types.KeyboardButton(config.CONTACT_BUTTON)
markup_MAIN.add(button_sales, button_promo, button_contact)


# keyboard categories
markup_CATEGORY = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
button_tech = types.KeyboardButton(config.TECH_BUTTON)
button_cloth = types.KeyboardButton(config.CLOTH_BUTTON)
button_domestic = types.KeyboardButton(config.DOMESTIC_BUTTON)
button_child = types.KeyboardButton(config.CHILD_BUTTON)
button_back = types.KeyboardButton(config.BACK_BUTTON)
button_food = types.KeyboardButton(config.FOOD_BUTTON)
button_other = types.KeyboardButton(config.OTHER_BUTTON)
markup_CATEGORY.add(button_tech, button_cloth, button_domestic, button_child, button_food, button_other, button_back)


@bot.message_handler(commands=["test_ad"])
def cmd_post(message):
	if message.chat.id == config.ADMIN:
		bot.send_message(message.chat.id, config.get_text(config.SRC_ADVERT), parse_mode = 'markdown')


@bot.message_handler(commands=["test_upd"])
def cmd_post(message):
	if message.chat.id == config.ADMIN:
		bot.send_message(message.chat.id, config.get_text(config.SRC_UPDATE), parse_mode = 'markdown')


@bot.message_handler(commands=["post_ad"])
def cmd_post(message):
	if message.chat.id == config.ADMIN:	
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		for row in c.execute("SELECT * FROM state"):
			out = "%s" % (row[0])
			last_msg = bot.send_message(int(out), config.get_text(config.SRC_ADVERT), parse_mode = 'markdown')
			print(last_msg.message_id)
			c.execute("UPDATE state SET last_msg_id = ? WHERE user_id = ?", (last_msg.message_id, out,))
			conn.commit()
		c.close()
		conn.close()


@bot.message_handler(commands=["post_upd"])
def cmd_post(message):
	if message.chat.id == config.ADMIN:
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		for row in c.execute("SELECT * FROM state"):
			out = "%s" % (row[0])
			last_msg = bot.send_message(int(out), config.get_text(config.SRC_UPDATE), parse_mode = 'markdown')
			c.execute("UPDATE state SET last_msg_id = ? WHERE user_id = ?", (last_msg.message_id, out,))
			conn.commit()
		c.close()
		conn.close()


@bot.message_handler(commands=["delete_post"])
def cmd_delete_post(message):
	if message.chat.id == config.ADMIN:
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		for row in c.execute("SELECT * FROM state WHERE last_msg_id <> 'None'"):
			out = "%s" % (row[0])
			msg_id = row[2]
			bot.delete_message(int(out), msg_id)
		c.close()
		conn.close()


@bot.message_handler(commands=["start"])
def cmd_start(message):
	state = get_state(message.chat.id)
	# IF PROMO AND SALES
	if state == config.States.S_PROMOSALES.value:
		set_state(message.chat.id, config.States.S_PROMOSALES.value)
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	# IF CATEGORIES
	elif state == config.States.S_CATEGORIES_PROMO.value or state == config.States.S_CATEGORIES_SALES.value:
		bot.send_message(message.chat.id, config.CATEGORY_ANSWER, reply_markup=markup_CATEGORY)
	#IF START
	else:
		bot.send_message(message.chat.id, "При возникновении проблем с ботом пропишите /start")
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
		set_state(message.chat.id, config.States.S_PROMOSALES.value)
	msg = Message(api_key = config.API_KEY, platform = config.PLATFORM, version = config.VERSION, user_id = str(message.chat.id), message = message.text, intent = "/start")
	msg.send() 


@bot.message_handler(func = lambda message: get_state(message.chat.id) == config.States.S_PROMOSALES.value)
def user_choosing_section(message):
	if message.text == config.PROMOCODES_BUTTON:
		set_state(message.chat.id, config.States.S_CATEGORIES_PROMO.value)
		bot.send_message(message.chat.id, config.CATEGORY_ANSWER, reply_markup=markup_CATEGORY)
	elif message.text == config.SALES_BUTTON:
		set_state(message.chat.id, config.States.S_CATEGORIES_SALES.value)
		bot.send_message(message.chat.id, config.CATEGORY_ANSWER, reply_markup=markup_CATEGORY)
	elif message.text == config.CONTACT_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_CONTACT), parse_mode = 'markdown')
	msg = Message(api_key = config.API_KEY, platform = config.PLATFORM, version = config.VERSION, user_id = str(message.chat.id), message = message.text)
	msg.send() 


@bot.message_handler(func = lambda message: get_state(message.chat.id) == config.States.S_CATEGORIES_PROMO.value)		
def user_choosing_promo_section(message):
	if message.text == config.TECH_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_PROMO_TECH), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.CLOTH_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_PROMO_CLOTH), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.DOMESTIC_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_PROMO_DOMESTIC), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.CHILD_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_PROMO_CHILD), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.FOOD_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_PROMO_FOOD), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.BACK_BUTTON:
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.OTHER_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_PROMO_OTHER), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	set_state(message.chat.id, config.States.S_PROMOSALES.value)
	msg = Message(api_key = config.API_KEY, platform = config.PLATFORM, version = config.VERSION, user_id = str(message.chat.id), message = message.text)
	msg.send() 


@bot.message_handler(func = lambda message: get_state(message.chat.id) == config.States.S_CATEGORIES_SALES.value)
def user_choosing_sale_section(message):
	if message.text == config.TECH_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_SALE_TECH), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.CLOTH_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_SALE_CLOTH), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.DOMESTIC_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_SALE_DOMESTIC), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.CHILD_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_SALE_CHILD), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.FOOD_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_SALE_FOOD), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.BACK_BUTTON:
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	elif message.text == config.OTHER_BUTTON:
		bot.send_message(message.chat.id, config.get_text(config.SRC_SALE_OTHER), parse_mode = 'markdown')
		bot.send_message(message.chat.id, config.MAIN_ANSWER, reply_markup=markup_MAIN)
	set_state(message.chat.id, config.States.S_PROMOSALES.value)
	msg = Message(api_key = config.API_KEY, platform = config.PLATFORM, version = config.VERSION, user_id = str(message.chat.id), message = message.text)
	msg.send() 


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
	'server.socket_host': WEBHOOK_LISTEN,
	'server.socket_port': WEBHOOK_PORT,
	'server.ssl_module': 'builtin',
	'server.ssl_certificate': WEBHOOK_SSL_CERT,
	'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})




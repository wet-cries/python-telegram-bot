from enum import Enum

token = '638899869:AAEc8sG8c7HCBNixvEwSi_TxZwy22kj2RMQ'


class States(Enum):
	S_START = "0"
	S_PROMOSALES = "1"
	S_CATEGORIES_PROMO = "2"
	S_CATEGORIES_SALES = "3"


def get_text(source):
	fd = open(source)
	tmp = fd.read()
	fd.close()
	return tmp


ADMIN = 320168389


# CHATBASE CONST
API_KEY = "e6873a67-8dbc-48e4-b39a-42ba02685ec9"
PLATFORM = "Telegram"
VERSION = "0.1"
INTENT = ''


# answers 
MAIN_ANSWER = "Выберите раздел, который вас интересует " + u"\u2B07"
CATEGORY_ANSWER = "Выберите категорию товаров, которая вас интересует " + u"\u2B07"


# Buttons preset
SALES_BUTTON = "Скидки и акции " + u"\u26A1"
PROMOCODES_BUTTON = "Промокоды " + u"\U0001F4A5"
CONTACT_BUTTON = "Связаться с нами " + u"\U0001F501"
CLOTH_BUTTON = "Одежда " + u"\U0001F455"
TECH_BUTTON = "Техника " + u"\U0001F4BB"
DOMESTIC_BUTTON = "Товары для дома " + u"\U0001F3E1"
CHILD_BUTTON = "Товары для детей " + u"\U0001F47C"
FOOD_BUTTON = "Еда " + u"\U0001F37D"
OTHER_BUTTON = "Прочее " + u"\U0001F6D2"
BACK_BUTTON = "Назад " + u"\U0001F519"


#  file sources
SRC_CONTACT = "../file/contact.txt"
SRC_PROMO_TECH = "../file/promo_tech.txt"
SRC_PROMO_CLOTH = "../file/promo_cloth.txt"
SRC_PROMO_DOMESTIC = "../file/promo_domestic.txt"
SRC_PROMO_CHILD = "../file/promo_child.txt"
SRC_PROMO_FOOD = "../file/promo_food.txt"
SRC_PROMO_OTHER = "../file/promo_other.txt"
SRC_SALE_TECH = "../file/sale_tech.txt"
SRC_SALE_CLOTH = "../file/sale_cloth.txt"
SRC_SALE_DOMESTIC = "../file/sale_domestic.txt"
SRC_SALE_CHILD = "../file/sale_child.txt"
SRC_SALE_FOOD = "../file/sale_food.txt"
SRC_SALE_OTHER = "../file/sale_other.txt"
SRC_UPDATE = "../file/update.txt"
SRC_ADVERT = "../file/advert.txt"

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from wiktionaryparser import WiktionaryParser
import re

# Put your token here
TOKEN = 
bot = TeleBot(TOKEN)

parser = WiktionaryParser()
parser.set_default_language("russian")
def to_text(obj):
	def dict_to_text(d):
		return "\n".join(f"{to_text(k).upper()}:\n\t{to_text(v)}\n" for k, v in d.items())
	def list_to_text(l):
		return "\n".join(to_text(i) for i in l) + "\n"
	if not obj: return ""
	if isinstance(obj, dict):
		return dict_to_text(obj)
	elif isinstance(obj, list):
		return list_to_text(obj)
	else: return str(obj)

def get_definition(word):
	result_dict = parser.fetch(word)
	return f"https://en.wiktionary.org/wiki/{word}\n {to_text(result_dict)}"

def create_markup(words):
	markup = InlineKeyboardMarkup()
	markup.add(*[InlineKeyboardButton(word, callback_data=word) for word in words])
	return markup

def get_words(text):
	return re.findall(r'[А-я]+', text)


@bot.message_handler(func=lambda m:True)
def nigger(message):
	bot.reply_to(message,"Click to search its definition on Wiktionary", reply_markup=create_markup(get_words(message.text.lower())))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	bot.edit_message_text(get_definition(call.data), call.message.chat.id, call.message.id, reply_markup=call.message.reply_markup)


bot.infinity_polling()

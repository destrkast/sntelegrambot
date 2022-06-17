import requests
from requests.auth import HTTPBasicAuth
import telebot
from telebot import types
import json
from types import SimpleNamespace

bot = telebot.TeleBot('5509854650:AAF07PoAUbZQVzplzRafo3BpihC6YJiNzII')

@bot.message_handler(commands=['start'])
def start(message):
  mess = f'Hello <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
  bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['sn'])
def sn(message):
  bot.send_message(message.chat.id, 'Before', parse_mode='html')
  # Set the request parameters
  url = 'https://dev77018.service-now.com/api/now/table/incident'

# Eg. User name="admin", Password="admin" for this code sample.
  user = 'admin'
  pwd = 'mgKW0!8GgY=u'

# Set proper headers
  headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
  value = message.from_user.first_name
  field = "short_description"
  data = {field: value}
  data_to_send = json.dumps(data)
  # '{"Machine Name": "machineA.host.com"}'

  response = requests.post(url, auth=(user, pwd), headers=headers , data=data_to_send)

# Check for HTTP codes other than 200
  # if response.status_code != 200:
  #   print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
  #   exit()

# Decode the JSON response into a dictionary and use the data
  data_recieved = response.json()
  print(data_recieved)
  bot.send_message(message.chat.id, data_recieved["result"]["number"])
  bot.send_message(message.chat.id, 'after', parse_mode='html')


# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#   if message.text == 'Hello':
#     bot.send_message(message.chat.id, 'Hello pidor!!!', parse_mode='html')
#   elif message.text == 'id':
#     bot.send_message(message.chat.id, f'Your ID: {message.from_user.id}', parse_mode='html')
#   elif message.text == 'photo':
#     photo = open('logo.png', 'rb')
#     bot.send_photo(message.chat.id, photo)
#   else:
#     bot.send_message(message.chat.id, "I don't understand", parse_mode='html')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
  bot.send_message(message.chat.id, "Cool photo DUDE!")

@bot.message_handler(commands=['website'])
def website(message):
  markup = types.InlineKeyboardMarkup()
  markup.add(types.InlineKeyboardButton('Follow the link', url='https://servicenow.com'))
  bot.send_message(message.chat.id, "Go to the website", reply_markup=markup)



@bot.message_handler(commands=['why'])
def why(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  yes = types.KeyboardButton('Yes')
  no = types.KeyboardButton('No')
  markup.add(yes, no)
  bot.send_message(message.chat.id, "Are you gay?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def reply_gif(message):
      if message.text == 'Yes':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'I knew', reply_markup=markup)
        video = open('gachi.mp4', 'rb')
        bot.send_document(message.chat.id, video)
      elif message.text == 'No':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Really?', reply_markup=markup)
        video = open('real.mp4', 'rb')
        bot.send_document(message.chat.id, video)



bot.polling(non_stop=True)
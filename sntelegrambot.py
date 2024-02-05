import requests
from requests.auth import HTTPBasicAuth
import telebot
from telebot import types
import json
from types import SimpleNamespace

bot = telebot.TeleBot("5509854650:AAF07PoAUbZQVzplzRafo3BpihC6YJiNzII")
user_login = ""
user_password = ""
payload = {}
# Flags to track function execution
description_called = False
urgency_called = False
short_description_called = False


@bot.message_handler(commands=["start"])
def start(message):
    mess = bot.send_message(
        message.chat.id,
        f"Hello <b>{message.from_user.first_name}</b>.\nPlease, provide login for your ServiceNow account",
        parse_mode="html",
    )
    bot.register_next_step_handler(mess, process_login)


def process_login(message):
    global user_login
    user_login = message.text
    bot.delete_message(message.chat.id, message_id=message.id)
    get_password(message)


def get_password(message):
    msg = bot.send_message(
        message.chat.id,
        "Please, provide password for your ServiceNow account",
        parse_mode="html",
    )
    bot.register_next_step_handler(msg, process_password)


def process_password(message):
    global user_password
    user_password = message.text
    bot.delete_message(message.chat.id, message_id=message.id)
    bot.send_message(
        message.chat.id,
        "Now you can get all incidents opened by you using /snget command or you can create a new one using /snpost command.",
        parse_mode="html",
    )


@bot.message_handler(commands=["snget"])
def snget(message):
    
    user = user_login
    pwd = user_password

    print(user, pwd)
    # Set the request parameters
    url = f"https://dev184100.service-now.com/api/now/table/incident?sysparm_query=caller_id.user_name%3D{user_login}&sysparm_display_value=true&sysparm_fields=number%2Cstate%2Curgency%2Cshort_description%2Ccaller_id.name%2Cassigned_to.name&sysparm_limit=5"

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP Request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code < 200 & response.status_code > 299:
        print(
            "Status:",
            response.status_code,
            "Headers:",
            response.headers,
            "Error Response:",
            response.json(),
        )
        exit()

    # Decode the JSON response into a dictionary and use the data
    data_recieved = response.json()
    print(data_recieved)

    for item in data_recieved["result"]:
        message_text = "\n".join(f"{key}: {value}" for key, value in item.items())
        bot.send_message(message.chat.id, message_text)

    # bot.send_message(message.chat.id, data_recieved["result"]["number"])


@bot.message_handler(commands=["snpost"])
def get_short_description(message):
    #Get short description, description and urgency
    mess = bot.send_message(
        message.chat.id,
        f"Please, provide short description for your incident request.",
        parse_mode="html",
    )
    bot.register_next_step_handler(mess, lambda m: build_payload(m, "short_description"))

def get_description(message):
    mess = bot.send_message(
        message.chat.id,
        f"Please, provide description for your incident request.",
        parse_mode="html",
    )
    bot.register_next_step_handler(mess, lambda m: build_payload(m, "description"))

def get_urgency(message):
    mess = bot.send_message(
        message.chat.id,
        f"Please, provide urgency for your incident request from 1 to 3 (1 - High, 2 - Medium, 3 - Low).",
        parse_mode="html",
    )
    bot.register_next_step_handler(mess, lambda m: build_payload(m, "urgency"))

def build_payload(message, field):
    global payload
    global description_called
    global short_description_called
    global urgency_called

    value = message.text
    payload[field] = value

    if "short_description" in payload and not short_description_called:
        get_description(message)
        short_description_called = True

    if "description" in payload and not description_called:
        get_urgency(message)
        description_called = True

    if "urgency" in payload and not urgency_called:
        send_post_request(message)
        urgency_called = True    

def send_post_request(message):
    print(payload)
    data_to_send = json.dumps(payload)
    # Eg. User name="admin", Password="admin" for this code sample.
    # user = "admin"
    # pwd = "avWu@7DW%A4b"
    user = user_login
    pwd = user_password
    # python sntelegrambot.py
    # Set the request parameters
    url = "https://dev184100.service-now.com/api/now/table/incident?sysparm_display_value=true&sysparm_fields=number%2Cshort_description%2Cdescription%2Curgency"

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers, data=data_to_send)

    # Check for HTTP codes other than 200
    if response.status_code < 200 & response.status_code > 299:
        print(
            "Status:",
            response.status_code,
            "Headers:",
            response.headers,
            "Error Response:",
            response.json(),
        )
        exit()

    # Decode the JSON response into a dictionary and use the data
    data_recieved = response.json()
    print(data_recieved)
    
    bot.send_message(message.chat.id,  f"An incident was created for you!",
        parse_mode="html")
    message_text = "\n".join(
        f"{key}: {value}" for key, value in data_recieved["result"].items()
    )
    bot.send_message(message.chat.id, message_text)


# response to photo
@bot.message_handler(content_types=["photo"])
def get_user_photo(message):
    bot.send_message(message.chat.id, "Cool photo DUDE!")


@bot.message_handler(commands=["website"])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Follow the link", url="https://dev184100.service-now.com/")
    )
    bot.send_message(message.chat.id, "Go to the website", reply_markup=markup)


@bot.message_handler(commands=["why"])
def why(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes = types.KeyboardButton("Yes")
    no = types.KeyboardButton("No")
    markup.add(yes, no)
    bot.send_message(message.chat.id, "Are you a human?", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def reply_gif(message):
    if message.text == "Yes":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "I knew", reply_markup=markup)
        video = open("gachi.mp4", "rb")
        bot.send_document(message.chat.id, video)
    elif message.text == "No":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Really?", reply_markup=markup)
        video = open("real.mp4", "rb")
        bot.send_document(message.chat.id, video)


bot.polling(non_stop=True)

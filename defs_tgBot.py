from re import X
# pip install pyTelegramBotAPI SpeechRecognition pydub
# pip install Pillow
# pip install python-dotenv

# from telebot.types import MessageEntity  #
import os
# import sys
import telebot
from telebot import types  # для указание типов
# import config
# import speech_recognition
# from pydub import AudioSegment
# from PIL import Image, ImageEnhance, ImageFilter
from dotenv.main import load_dotenv

import classes
from classes import CreateMenu, user_add, get_user
from datetime import datetime, timedelta
import time
import locale


# Создаем глобальную переменную - множество,  состоящем из словарей вошедших в тг бот пользователей по их id.
# (id: ( FirstName, DateTimeFirst, DataTimeLast, Language))


# Проверяем локальные настройки и часовой пояс, может отличаться на разных серверах, а нам нужно выводить Московское время
locale.setlocale(locale.LC_ALL, "")
lc = locale.getlocale()
if time.tzname[0] == 'UTC':
    my_timedelta = 3
else:
    my_timedelta = 0
print(lc, time.tzname[0])
now = datetime.now() + timedelta(hours=my_timedelta)
dt_in = now.strftime("%H:%M %d.%m.%Y")
print('===========  тг бот запущен', dt_in, '===========')
# Читаем переменные из env
load_dotenv()
token = os.environ['TOKEN_TGBOT']  # <<< Ваш токен
# print(token)
# sys.exit("Exit 47")
bot = telebot.TeleBot(token)
# Формируем словари главного и подменю на разных языках.
cm = CreateMenu('list_menu.xlsx')
btn_list1_RUS = cm.select_button('main')
cm_data_dict_RUS = cm.select_button('Level_1')
btn_list1_ENG = cm.select_button('main', 'ENG')
cm_data_dict_ENG = cm.select_button('Level_1', 'ENG')

users_dict = dict()

btn_list1 = btn_list1_RUS
cm_data_dict = cm_data_dict_RUS
language = 'RUS'


# btn_list = cm.select_button('Level_1')


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    now = datetime.now() + timedelta(hours=my_timedelta)
    dt_in = now.strftime("%H:%M %d.%m.%Y")
    print(dt_in, ';', message.from_user.id, ';', message.from_user.first_name)


    # global btn_list1
    # global cm_data_dict

    # Обработка поступившего user.id
    global users_dict
    cur_user = classes.get_user(message.from_user.id, users_dict, message.from_user.first_name)
    print('--- say_hi --- ',cur_user)
    classes.user_add(cur_user, users_dict)
    print(users_dict)
    print(users_dict[message.from_user.id])
    cur_language = cur_user.Language
    cur_user.UpdateLanguage(cur_language)
    cur_user.UpdateDateTimeLast()
    classes.user_add(cur_user, users_dict)

    print(message.from_user.id, users_dict[message.from_user.id].Language)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # types.InlineKeyboardMarkup()

    if cur_language == 'RUS':
        btn_list1 = btn_list1_RUS
        # cm_data_dict = cm_data_dict_RUS
        text = (
            " Привет, {0.first_name}! Я бот помощник.\nПомогаю хорошему разработчику, Павлу Федорову, рассказать о себе тем, кому он может быть полезен."
            "\nНажимайте кнопки для получения информации."
            "\nНажав кнопку <узнать больше>, Вы попадете в более расширенное меню.").format(
            message.from_user)
    else:
        btn_list1 = btn_list1_ENG
        # cm_data_dict = cm_data_dict_ENG
        text = (
            "Hello, {0.first_name}! I'm an assistant bot.\nI'm helping a good developer, Pavel Fedorov, tell about himself to those who might find him useful."
            "\nPress buttons for information."
            "\nClicking the <To learn more> button will take you to a more advanced menu.").format(
            message.from_user)

    list_row_button = []
    for element in btn_list1.items():
        btn = types.KeyboardButton(element[0])
        list_row_button.append(btn)
    # формируем кнопки в строки по 3 штуки
    i_max = len(list_row_button) // 3 + 1
    # print(i_max)
    for i in range(i_max):
        row_button = list_row_button[3 * i:3 + (i * 3)]
        markup.row(*row_button)


    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    print(message.text)
    # print(type(cm.data))
    # print(cm.data)
    # cm_data_dict = cm.select_button('Level_1')
    # print(cm_data_dict)
    global users_dict

    # global btn_list1
    # global cm_data_dict

    cur_user = classes.get_user(message.from_user.id, users_dict, message.from_user.first_name)
    print('--- func 1---', cur_user, cur_user.Language, message.from_user.id)
    classes.user_add(cur_user, users_dict)
    cur_language = cur_user.Language


    if cur_language == 'RUS':
        cm_data_dict = cm_data_dict_RUS
        text1 = "Нажми кнопку, чтобы получить информацию по интересующему вопросу."
    else:
        cm_data_dict = cm_data_dict_ENG
        text1 = "Click the button to receive information on the issue of interest."

    if message.text in ("Назад", "Back"):
        say_hi(message)

    elif (message.text in ("Узнать больше", "To learn more")):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # types.InlineKeyboardMarkup()
        btn_list = cm_data_dict  # здесь подумать
        # btn_list1 = btn_list
        list_row_button = []
        for element in btn_list.items():
            btn = types.KeyboardButton(element[0])
            list_row_button.append(btn)
        # формируем кнопки в строки по 3 штуки
        i_max = len(list_row_button) // 3 + 1
        print(i_max)
        for i in range(i_max):
            row_button = list_row_button[3 * i:3 + (i * 3)]
            markup.row(*row_button)
        bot.send_message(message.chat.id, text=text1,
                         reply_markup=markup)

    elif (message.text == "RUS"):
        cur_language = 'RUS'
        cur_user.UpdateLanguage(cur_language)
        classes.user_add(cur_user, users_dict)
        print('--- func 2 ---', cur_user, cur_user.Language, message.from_user.id)
        cm_data_dict = cm_data_dict_RUS
        say_hi(message)

    elif (message.text == "ENG"):
        cur_language = 'ENG'
        cur_user.UpdateLanguage(cur_language)
        classes.user_add(cur_user, users_dict)
        print('--- func 3 ---', cur_user, cur_user.Language, message.from_user.id)
        cm_data_dict = cm_data_dict_ENG
        say_hi(message)

    elif (message.text in ("Фото", 'Photo')):
        photos_to_send = open('Fedorov_P_21.jpg', 'rb')
        bot.send_photo(message.chat.id, photos_to_send)

    # elif (message.text == "Отзывы"):
    #     photos_to_send = open('Otz1.jpg', 'rb')
    #     bot.send_photo(message.chat.id, photos_to_send)

    # Доработать , добавив признак обработки (jpg, pdf), чтобы обработка происходила без hard кода.
    # Имя файла и тип обработки читался из словаря на основе настроечного файла XLS.
    elif (message.text in ("Обучение, курсы", "Training, courses")):
        photos_to_send = open('refresher_courses.jpg', 'rb')
        bot.send_photo(message.chat.id, photos_to_send)

    elif (message.text in ("Файл с резюме", "Resume file")):
        doc_to_send = open('Pavel_Fedorov_Staff_eng.pdf', 'rb')
        bot.send_document(chat_id=message.chat.id, document=doc_to_send)

    elif (message.text in cm_data_dict):
        text = cm_data_dict[message.text]
        bot.send_message(message.chat.id, text)

    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммировал..")


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)


# Запускаем бота. Он будет работать до тех пор, пока работает ячейка (крутится значок слева).
# Для остановки бота надо прервать выполнение программы. Ctrl-C или по другому.
bot.infinity_polling()

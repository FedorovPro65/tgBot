from re import X
# pip install pyTelegramBotAPI SpeechRecognition pydub
# pip install Pillow
# pip install python-dotenv

from telebot.types import MessageEntity  #
import os
import sys
import telebot
from telebot import types  # для указание типов
# import config
import speech_recognition
from pydub import AudioSegment
from PIL import Image, ImageEnhance, ImageFilter
from dotenv.main import load_dotenv
from classes import CreateMenu
from datetime import datetime, timedelta
import time
import locale

# Проверяем локальные настройки и часовой пояс, может отличаться на разных серверах, а нам нужно выводить Московское время
locale.setlocale(locale.LC_ALL, "")
lc = locale.getlocale()
if time.tzname[0] == 'UTC':
    my_timedelta = 3
else:
    my_timedelta = 0
print(lc,time.tzname[0])
now = datetime.now() + timedelta(hours=my_timedelta)
dt_in = now.strftime("%H:%M %d.%m.%Y")
print('===========  тг бот запущен', dt_in, '===========')
# Читаем переменные из env
load_dotenv()
token = os.environ['TOKEN_TGBOT']  # <<< Ваш токен
# print(token)
# sys.exit("Exit 47")
bot = telebot.TeleBot(token)
cm = CreateMenu('list_menu.xlsx')
btn_list1 = cm.select_button('main')
cm_data_dict = cm.select_button('Level_1')


# btn_list = cm.select_button('Level_1')

def transform_image(filename):
    # Функция обработки изображения
    source_image = Image.open(filename)
    enhanced_image = source_image.filter(ImageFilter.EMBOSS)
    enhanced_image = enhanced_image.convert('RGB')
    enhanced_image.save(filename)
    return filename


def resize_image(filename, n: int = 2):
    # Функция уменьшения размера изображения в n раз
    source_image = Image.open(filename)
    width = source_image.size[0]
    height = source_image.size[1]
    enhanced_image = source_image.resize((width // n, height // n))
    enhanced_image.save(filename)
    return filename


@bot.message_handler(content_types=['photo'])
def resend_photo(message):
    # Функция отправки обработанного изображения
    file_id = message.photo[-1].file_id
    x = str(message.caption)
    try:
        n = int(x)
    except:
        n = 3
    filename = download_file(bot, file_id)

    # Трансформируем изображение
    # transform_image(filename)
    resize_image(filename, n)

    message_caption = 'Картинка уменьшена в ' + str(n) + ' раз.'
    image = open(filename, 'rb')
    bot.send_photo(message.chat.id, image, message_caption)
    image.close()

    # Не забываем удалять ненужные изображения
    if os.path.exists(filename):
        os.remove(filename)


def oga2wav(filename):
    # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    # Скачивание файла, который прислал пользователь
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    now = datetime.now() + timedelta(hours=my_timedelta)
    dt_in = now.strftime("%H:%M %d.%m.%Y")
    print(dt_in, ';', message.from_user.id, ';', message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # types.InlineKeyboardMarkup()
    # btn_list = cm.select_button('main')
    # btn_list1 = btn_list
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

    text = "Привет, {0.first_name}! Я бот помощник.\n Помогаю хорошему разработчику, Павлу Федорову, рассказать о себе тем, кому он может быть полезен.\n Нажимайте кнопки для получения информации.\n Нажав - узнать больше, Вы попадете в более расширенное меню".format(
        message.from_user)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    print(message.text)
    # print(type(cm.data))
    # print(cm.data)
    # cm_data_dict = cm.select_button('Level_1')
    # print(cm_data_dict)
    if (message.text == "Назад"):
        say_hi(message)
    elif (message.text == "Узнать больше"):
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
        bot.send_message(message.chat.id, text="Нажми кнопку, чтобы получить информацию по интересующему вопросу.",
                         reply_markup=markup)

    elif (message.text == "Фото"):
        photos_to_send = open('Fedorov_P_21.jpg', 'rb')
        bot.send_photo(message.chat.id, photos_to_send)

    # elif (message.text == "Отзывы"):
    #     photos_to_send = open('Otz1.jpg', 'rb')
    #     bot.send_photo(message.chat.id, photos_to_send)

    # Доработать , добавив признак обработки (jpg, pdf), чтобы обработка происходила без hard кода.
    # Имя файла и тип обработки читался из словаря на основе настроечного файла XLS.
    elif (message.text == "Обучение, курсы"):
        photos_to_send = open('refresher_courses.jpg', 'rb')
        bot.send_photo(message.chat.id, photos_to_send)

    elif (message.text == "Файл с резюме"):
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
bot.polling()

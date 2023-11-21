from re import X
# pip install pyTelegramBotAPI SpeechRecognition pydub
# pip install Pillow
# pip install python-dotenv

from telebot.types import MessageEntity #
import os
import sys
import telebot
from telebot import types # для указание типов
# import config
import speech_recognition
from pydub import AudioSegment
from PIL import Image, ImageEnhance, ImageFilter
from dotenv.main import load_dotenv

# Читаем переменные из env
load_dotenv()
token = os.environ['TOKEN_TGBOT']  # <<< Ваш токен
# print(token)
# sys.exit("Exit 47")
bot = telebot.TeleBot(token)

def transform_image(filename):
    # Функция обработки изображения
    source_image = Image.open(filename)
    enhanced_image = source_image.filter(ImageFilter.EMBOSS)
    enhanced_image = enhanced_image.convert('RGB')
    enhanced_image.save(filename)
    return filename

def resize_image(filename, n:int = 2 ):
    # Функция уменьшения размера изображения в n раз
    source_image = Image.open(filename)
    width = source_image.size[0]
    height = source_image.size[1]
    enhanced_image= source_image.resize((width//n, height//n))
    enhanced_image.save(filename)
    return filename

@bot.message_handler(content_types=['photo'])
def resend_photo(message):
    # Функция отправки обработанного изображения
    file_id = message.photo[-1].file_id
    x = str(message.caption)
    try :
      n = int(x)
    except :
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
    # bot.send_message(message.chat.id, 'Привет')
    # markup = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
    # markup.add(button1)
    # bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user), reply_markup=markup)
    #
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я добрый бот habr.com".format(
                        message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}!.. \n Рад общению с тобой!)")
    elif (message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "Меня зовут Батяня..")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text=" Поприветствовать гостя.\n Ответить на некоторые вопросы."
                                               "\n Уменьшить размер картинки из файла, который ты мне отправишь.\n Выдать текст твоего звукового сообщения.")

    elif (message.text == "Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
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


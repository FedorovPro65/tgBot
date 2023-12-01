import pandas as pd
import telebot
from telebot import types  # для указание типов
from typing import List
from datetime import datetime
import time

class BotUser:
    def __init__(self, UserId, UserName):
        self.UserId = UserId
        self.UserName = UserName
        self.DateTimeFirst = datetime.now()
        self.DateTimeLast = self.DateTimeFirst  # Дата время Последнего входа пользователя
        self.Language = 'RUS'

    def UpdateDateTimeLast(self):
        # Присваивает текущее значение дата время для параметра DateTimeLast
        self.DateTimeLast = datetime.now()
        # print(self.DateTimeLast)

    def UpdateLanguage(self, Language: str):
        # Присваивает текущее значение дата время для параметра DateTimeLast
        self.Language = Language
        # print(self.Language)

    def UpdateOLdUser(self, UsersDict:dict, user_id: int):

        self.UserName = UsersDict[user_id].UserName
        self.DateTimeFirst = UsersDict[user_id].DateTimeFirst
        self.DateTimeLast = datetime.now()  # Дата время Последнего входа пользователя
        self.Language = UsersDict[user_id].Language

    def __str__(self) -> str:
        return (
            f'Point(id = {self.UserId}, FirstName: {self.UserName},DateTimeFirst: {self.DateTimeFirst.strftime("%H:%M:%S %d.%m.%y")}'
            f', DateTimeLast: {self.DateTimeLast.strftime("%H:%M:%S %d.%m.%y")}, Language: {self.Language})')


def user_add(user: BotUser, Mydict: dict):
    ''' Добавляем user в словарь пользователей, по любому, если нет строки - создастся, если есть - обновится '''
    i = user.UserId
    Mydict[i] = user

def get_user(user_id:int, Mydict: dict, user_name = 'None'):
    ''' возвращает текущего user по user_id, данные берутся из справочника пользователей если он есть в справочнике,
    иначе - создается новый пользователь'''
    if user_id in Mydict:
        my_user = BotUser(user_id,'OldUserName')
        my_user.UpdateOLdUser(Mydict, user_id)  # заполняем поля старого из словаря
    else:
        my_user = BotUser(user_id, user_name) # создаем нового
    return my_user

def Ptlf(str_to_log_file:str):
    with open("log.txt", "a", encoding='utf-8') as f:
        str_to_log_file = str_to_log_file + '\n'
        sf = f.write(str_to_log_file)
class CreateMenu:
    def __init__(self, filename):
        '''Конструктор класса. Создает DataFrame с данными для кнопок меню.'''
        # self.__db_path = os.getcwd()
        # self.db_name = os.path.join(self.__db_path, 'database.db')
        self.filename = filename  # 'list_menu.xlsx'
        # Read the values of the file in the dataframe
        self.data = pd.DataFrame(pd.read_excel(filename),
                                 columns=['type_menu', 'order_num', 'type_btn', 'btn_name', 'btn_callback',
                                          'btn_name_eng', 'btn_callback_eng'])

    def select_button(self, type_menu: str, lng='RUS') -> dict:
        '''В качестве аргумента принимает "тип меню" и язык меню. Возвращает словарь где ключ = текст кнопки, значение = callbackdata кнопки'''

        result = dict()
        data = self.data
        df = data[data['type_menu'] == type_menu][
            ['btn_name', 'order_num', 'type_btn', 'btn_callback', 'btn_name_eng', 'btn_callback_eng']].head(13)
        # print('---', type(df), df.count())
        # print(df)

        df = df.reset_index()  # make sure indexes pair with number of rows
        for index, row in df.iterrows():
            # print('----', row['btn_name'], '--', row['btn_callback'])
            if lng == 'RUS':
                result[row['btn_name']] = (row['btn_callback'], row['type_btn'])
            else:
                result[row['btn_name_eng']] = (row['btn_callback_eng'], row['type_btn'])
        print('Словарь для меню', type_menu, 'создан')
        return result


if __name__ == '__main__':
    # cm = CreateMenu('list_menu.xlsx')
    # btn_list1 = cm.select_button('Level_1','ENG')
    # print(btn_list1)

    # создаем экземпляр объекта
    # указываем имя лога и
    # PRINT_TO_FILE = True - вывод в файл,
    # иначе - на консоль
    # log = mylogger('LOGFILE.txt', True)
    #
    # # переопределяем адрес функции print()
    # # на адрес метода нашего логгера
    # print = log.printml
    #
    # d1 = dict()
    # u1 = BotUser(12, 'Ivan')
    # user_add(u1, d1)
    # time.sleep(3)
    # u1.UpdateDateTimeLast()
    # user_add(u1, d1)
    # u1 = BotUser(14, 'Ani')
    # u1.UpdateLanguage('ENG')
    # user_add(u1, d1)
    # for d in d1.keys():
    #     print(d1[d])
    # print(d1[14].Language)
    # cur_user = get_user(12,d1)
    # print(cur_user.UserId,cur_user.Language)

    Ptlf('jfjfj')



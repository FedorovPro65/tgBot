import pandas as pd
import telebot
from telebot import types # для указание типов
class CreateMenu:
    def __init__(self,filename):
        '''Конструктор класса. Создает DataFrame с данными для кнопок меню.'''
        # self.__db_path = os.getcwd()
        # self.db_name = os.path.join(self.__db_path, 'database.db')
        self.filename = filename # 'list_menu.xlsx'
        # Read the values of the file in the dataframe
        self.data = pd.DataFrame(pd.read_excel(filename), columns=['type_menu', 'order_num', 'btn_name', 'btn_callback'])


    def select_button(self, type_menu: str) -> dict:
        '''В качестве аргумента принимает "тип меню". Возвращает словарь где ключ = текст кнопки, значение = callbackdata кнопки'''

        result = dict()
        data = self.data
        df = data[data['type_menu'] == type_menu][['btn_name', 'btn_callback']].head(13)
        # print('---', type(df), df.count())
        # print(df)

        df = df.reset_index()  # make sure indexes pair with number of rows
        for index, row in df.iterrows():
            # print('----', row['btn_name'], '--', row['btn_callback'])
            result[row['btn_name']] = row['btn_callback']
        print('Словарь для меню', type_menu, 'создан')
        return result


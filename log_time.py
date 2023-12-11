from datetime import datetime
import time

# Пишет в файл время каждые s_sleep секунд. Для анализа, когда упала программа.
print('--------------')
s_sleep = 600
i = 0
i_max = 720
with open("FileTest1.txt", 'a') as f:
    f.write(f'---------------- Start in  {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}\n')
for i in range(i_max):
    time.sleep(s_sleep)
    cur_time = datetime.now()
    cur_time_str = cur_time.strftime("%H:%M:%S %d.%m.%Y")
    with open("FileTest1.txt", 'a') as f:
        f.write(f'{i}, {cur_time_str}\n')



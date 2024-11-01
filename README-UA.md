# PAWS

[![Static Badge](https://img.shields.io/badge/Telegram-BOT-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/PAWSOG_bot/PAWS?startapp=8ppTr9Ft)

[![Static Badge](https://img.shields.io/badge/My_Telegram_Сhannel-@CryptoCats__tg-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/CryptoCats_tg)

## Рекомендація перед використанням

# 🔥🔥 Використовуйте PYTHON 3.10-3.11 🔥🔥

[![Static Badge](https://img.shields.io/badge/README_in_Ukrainian_available-README_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D1%81%D1%8C%D0%BA%D0%BE%D1%8E_%D0%BC%D0%BE%D0%B2%D0%BE%D1%8E-blue.svg?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjgwMCI+DQo8cmVjdCB3aWR0aD0iMTIwMCIgaGVpZ2h0PSI4MDAiIGZpbGw9IiMwMDU3QjciLz4NCjxyZWN0IHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjQwMCIgeT0iNDAwIiBmaWxsPSIjRkZENzAwIi8+DQo8L3N2Zz4=)](README-UA.md)
[![Static Badge](https://img.shields.io/badge/README_in_russian_available-README_%D0%BD%D0%B0_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B5-blue?style=for-the-badge)](README-RU.md)


## Функціонал
| Функціонал                                                     | Підтримується |
|----------------------------------------------------------------|:---------:|
| Багатопоточність                                               |     ✅     |
| Прив'язка проксі до сесії                                      |     ✅     |
| Привязка User-Agent до сесії                                   |     ✅     |
| Автоматична реєстрація акаунта з вашим реферальним кодом       |     ✅     |
| Виконання завдань  		 	              			         |     ✅     |
| Випадковий час сну між акаунтами                               |     ✅     |
| Підтримка pyrogram .session                                    |     ✅     |

## [Налаштування](https://github.com/CatSnowdrop/PAWS/blob/main/.env-example/)
|           Налаштування        |                                       Опис                                            |
|:-----------------------------:|:-------------------------------------------------------------------------------------:|
|         **API_ID**            |        Ваш Telegram API ID (ціле число)                                               |
|         **API_HASH**          |        Ваш Telegram API Hash (рядок)                                                  |
|          **LANG**             |        Мова інтерфейсу (EN / RU / UA)                                                 |
|        **AUTO_TASKS**         |        Автоматично виконувати завдання (True / False)                                 |
|   **TASKS_JOIN_TO_CHANNEL**   |        Виконувати завдання з підпискою на канал/чат (True / False)                    |
|     **DELAY_GET_TASKS**       |        Затримка після отримання списку завдань (напр., [5, 10])                       |
|   **DELAY_TASK_COMPLETE**     |        Затримка після виконання завдання (напр., [10, 15])                            |
|     **DELAY_TASK_CLAIM**      |        Затримка після отримання нагороди за завдання (напр., [10, 15])                |
|      **BLACKLIST_TASK**       |        Чорний список завдань (напр., ["Connect wallet", "Invite 10 friends"])         |
|  **USE_RANDOM_DELAY_IN_RUN**  |        Використовувати випадкову затримку під час запуску (True / False)              |
|      **DELAY_ACCOUNT**        |        Випадкова затримка під час запуску (напр., [0, 15])                            |
|      **DELAY_RELOGIN**        |        Затримка після невдалої спроби входу (напр., [0, 15])                          |
|    **DELAY_RESTARTING**       |        Затримка перед повторним запуском програми (напр., [21600, 43200])             |
|         **USE_REF**           |        Чи використовувати рефреральне посилання (True / False)                        |
|         **REF_LINK**          |        Реферальне посилання                                                           |
|  **USE_PROXY_FROM_FILE**      |        Використовувати проксі з `bot/config/proxies.txt` (True / False). Інакше використовується проксі з `sessions/accounts.json`|


## Швидкий старт 📚
Windows: Для швидкого встановлення і подальшого запуску - запустіть файл run.bat

Linux: Для швидкого встановлення і подальшого запуску - запустіть файл run.sh

## Попередні умови
Перш ніж почати, переконайтеся, що у вас встановлено наступне:
- [Python](https://www.python.org/downloads/) **версії 3.10-3.11**

## Отримання API ключів
1. Перейдіть на сайт my.telegram.org і увійдіть у систему, використовуючи свій номер телефону.
2. Виберіть "API development tools" і заповніть форму для реєстрації нового додатка.

## Установка
Ви можете завантажити [**Репозиторій**](https://github.com/CatSnowdrop/PAWS) клонуванням на вашу систему і встановленням необхідних залежностей:
```shell
git clone https://github.com/CatSnowdrop/PAWS.git
cd PAWS
```

Потім для автоматичного встановлення введіть:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```


# Linux ручне встановлення
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

Також для швидкого запуску ви можете використовувати аргументи, наприклад:
```shell
~/PAWS >>> python3 main.py --action (1/2)
# Or
~/PAWS >>> python3 main.py -a (1/2)

# 1 - Запустити софт
# 2 - Створити сесію
```

# Windows ручне встановлення
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Також для швидкого запуску ви можете використовувати аргументи, наприклад:
```shell
~/PAWS >>> python main.py --action (1/2)
# Or
~/PAWS >>> python main.py -a (1/2)

# 1 - Запустити софт
# 2 - Створити сесію
```

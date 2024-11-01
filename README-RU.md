# PAWS

[![Static Badge](https://img.shields.io/badge/Telegram-BOT-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/PAWSOG_bot/PAWS?startapp=8ppTr9Ft)

[![Static Badge](https://img.shields.io/badge/My_Telegram_Сhannel-@CryptoCats__tg-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/CryptoCats_tg)

## Рекомендация перед использованием

# 🔥🔥 Используйте PYTHON 3.10-3.11 🔥🔥

[![Static Badge](https://img.shields.io/badge/README_in_Ukrainian_available-README_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D1%81%D1%8C%D0%BA%D0%BE%D1%8E_%D0%BC%D0%BE%D0%B2%D0%BE%D1%8E-blue.svg?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjgwMCI+DQo8cmVjdCB3aWR0aD0iMTIwMCIgaGVpZ2h0PSI4MDAiIGZpbGw9IiMwMDU3QjciLz4NCjxyZWN0IHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjQwMCIgeT0iNDAwIiBmaWxsPSIjRkZENzAwIi8+DQo8L3N2Zz4=)](README-UA.md)
[![Static Badge](https://img.shields.io/badge/README_in_russian_available-README_%D0%BD%D0%B0_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B5-blue?style=for-the-badge)](README-RU.md)


## Функционал
| Функционал                                                     | Поддерживается |
|----------------------------------------------------------------|:---------:|
| Многопоточность                                                |     ✅     |
| Привязка прокси к сессии                                       |     ✅     |
| Привязка User-Agent к сессии                                   |     ✅     |
| Автоматическая регистрация аккаунта с вашим реферальным кодом  |     ✅     |
| Выполнение заданий		 	              			         |     ✅     |
| Случайное время сна между аккаунтами                           |     ✅     |
| Поддержка pyrogram .session                                    |     ✅     |

## [Настройки](https://github.com/CatSnowdrop/PAWS/blob/main/.env-example/)
|           Настройка           |                                       Описание                                        |
|:-----------------------------:|:-------------------------------------------------------------------------------------:|
|         **API_ID**            |        Ваш Telegram API ID (целое число)                                              |
|         **API_HASH**          |        Ваш Telegram API Hash (строка)                                                 |
|          **LANG**             |        Язык интерфейса (EN / RU / UA)                                                 |
|        **AUTO_TASKS**         |        Автоматически выполнять задания (True / False)                                 |
|   **TASKS_JOIN_TO_CHANNEL**   |        Выполнять задания с подпиской на канал/чат (True / False)                      |
|     **DELAY_GET_TASKS**       |        Задержка после получения списка заданий (напр., [5, 10])                       |
|   **DELAY_TASK_COMPLETE**     |        Задержка после выполнения задания (напр., [10, 15])                            |
|     **DELAY_TASK_CLAIM**      |        Задержка после получения награда за задание (напр., [10, 15])                  |
|      **BLACKLIST_TASK**       |        Чёрный список заданий (напр., ["Connect wallet", "Invite 10 friends"])         |
|  **USE_RANDOM_DELAY_IN_RUN**  |        Использовать случайную задержку при запуске (True / False)                     |
|      **DELAY_ACCOUNT**        |        Случайная задержка при запуске (напр., [0, 15])                                |
|      **DELAY_RELOGIN**        |        Задержка после неудачной попытки входа (напр., [0, 15])                        |
|    **DELAY_RESTARTING**       |        Задержка перед повторным запуском программы (напр., [21600, 43200])            |
|         **USE_REF**           |        Использовать ли рефреральную ссылку (True / False)                             |
|         **REF_LINK**          |        Реферальная ссылка                                                             |
|  **USE_PROXY_FROM_FILE**      |        Использовать прокси из `bot/config/proxies.txt` (True / False). Иначе используется прокси из `sessions/accounts.json`|


## Быстрый старт 📚
Windows: Для быстрой установки и последующего запуска - запустите файл run.bat

Linux: Для быстрой установки и последующего запуска - запустите файл run.sh

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.10-3.11**

## Получение API ключей
1. Перейдите на сайт my.telegram.org и войдите в систему, используя свой номер телефона.
2. Выберите "API development tools" и заполните форму для регистрации нового приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/CatSnowdrop/PAWS) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/CatSnowdrop/PAWS.git
cd PAWS
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```


# Linux ручная установка
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/PAWS >>> python3 main.py --action (1/2)
# Or
~/PAWS >>> python3 main.py -a (1/2)

# 1 - Запустить софт
# 2 - Создать сессию
```

# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/PAWS >>> python main.py --action (1/2)
# Or
~/PAWS >>> python main.py -a (1/2)

# 1 - Запустить софт
# 2 - Создать сессию
```

import asyncio
import random
import string
import time
from urllib.parse import unquote, quote

from bot.config import settings
from bot.utils import logger, load_from_json, add_list_to_json
from bot.exceptions import InvalidSession
from .agents import generate_random_user_agent
from .headers import headers

import aiohttp
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy

from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.errors import (Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait, UserDeactivatedBan,
                             AuthKeyDuplicated, SessionExpired, SessionRevoked)


from faker import Faker

async def run_tapper(thread: int, session_name: str, proxy: [str, None]):
    try:
        await Tapper(thread=thread, session_name=session_name, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")

def retry_async(max_retries=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            thread, account = args[0].thread, args[0].account
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if settings.LANG == 'RU':
                        logger.error(f"Поток {thread} | {account} | Ошибка: {e}. Повторная попытка {retries}/{max_retries}...")
                    elif settings.LANG == 'UA':
                        logger.error(f"Поток {thread} | {account} | Помилка: {e}. Повторна спроба {retries}/{max_retries}...")
                    else:
                        logger.error(f"Thread {thread} | {account} | Error: {e}. Retrying {retries}/{max_retries}...")
                    await asyncio.sleep(10)
                    if retries >= max_retries:
                        break
        return wrapper
    return decorator


class Tapper:
    def __init__(self, thread: int, session_name: str, proxy: [str, None]):
        self.LANG = settings.LANG
        self.account = session_name + '.session'
        self.thread = thread
        if settings.USE_REF:
            self.ref_token = '8ppTr9Ft' if random.random() <= 0.3 else settings.REF_LINK.split('=')[1]
        else:
            self.ref_token = ''
        self.proxy = proxy
        connector = ProxyConnector().from_url(proxy) if proxy else None

        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client = Client(
            name=session_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            workdir='sessions/',
            proxy=proxy_dict,
            lang_code='ru'
        )

        headers['User-Agent'] = self.get_user_agent(session_name)
        headers["Origin"] = "https://app.paws.community"
        headers["Referer"] = "https://app.paws.community/"

        self.headers = headers

        self.session = CloudflareScraper(headers=headers, connector=connector)


    def get_user_agent(self, session_name):
        file = 'sessions/accounts.json'
        accounts_from_json = load_from_json(file)
        user_agent_str = None
        for saved_account in accounts_from_json:
            if saved_account['session_name'] == session_name:
                if 'user_agent' in saved_account:
                    user_agent_str = saved_account['user_agent']
        if user_agent_str != None and user_agent_str != "":
            return user_agent_str
        else:
            user_agent_str = generate_random_user_agent(device_type='android', browser_type='chrome')
            add_list_to_json(file, 'session_name', session_name, 'user_agent', user_agent_str)
            return user_agent_str


    async def logout(self):
        await self.session.close()


    async def check_proxy(self):
        try:
            resp = await self.session.get('https://api.ipify.org?format=json', timeout=aiohttp.ClientTimeout(5))
            ip = (await resp.json()).get('ip')
            logger.info(f"Thread {self.thread} | {self.account} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"Thread {self.thread} | Proxy: {self.proxy} | Error: {error}")


    async def need_new_login(self):
        if (await self.session.get("https://api.paws.community/v1/user/leaderboard?page=0&limit=100")).status == 200:
            return False
        else:
            return True


    async def claim_task(self, task_id: str, task_name: str, reward: str):
        try:
            resp = await self.session.post("https://api.paws.community/v1/quests/claim", json={"questId":task_id})
            resp_json = await resp.json()
            success = resp_json.get("success")
            data = resp_json.get("data")
            if success and data:
                if self.LANG == 'RU':
                    logger.success(f"Поток {self.thread} | {self.account} | За задание «{task_name}» получена награда: {reward}")
                elif self.LANG == 'UA':
                    logger.success(f"Поток {self.thread} | {self.account} | За завдання «{task_name}» отримано нагороду: {reward}")
                else:
                    logger.success(f"Thread {self.thread} | {self.account} | A reward has been received for the task «{task_name}»: {reward}")
                return True
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Не удалось получить награду за задание «{task_name}»")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Не вдалося отримати нагороду за завдання «{task_name}»")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Failed to get the reward for the task «{task_name}»")
                return False
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при выполнении задания: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час виконання завдання: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error in completing the task: {e}")
            return False


    async def join_to_tg_channel(self, chat) -> dict[str]:
        try:
            with_tg = True
            if not self.tg_client.is_connected:
                with_tg = False
                await self.tg_client.connect()
            if 't.me/' in chat:
                chat = chat.split('t.me/')[1]
            return_chat = await self.tg_client.join_chat(chat)
            if with_tg is False:
                await self.tg_client.disconnect()
            return return_chat
        except Exception as error:
            logger.error(f"Thread {self.thread} | {self.account} | Unknown error when join_to_tg_channel: {error} | ")
            await asyncio.sleep(delay=3)


    async def complete_task(self, task_id: str, task_name: str):
        try:
            resp = await self.session.post("https://api.paws.community/v1/quests/completed", json={"questId":task_id})
            resp_json = await resp.json()
            success = resp_json.get("success")
            data = resp_json.get("data")
            if success and data:
                if self.LANG == 'RU':
                    logger.success(f"Поток {self.thread} | {self.account} | Задание «{task_name}» выполнено")
                elif self.LANG == 'UA':
                    logger.success(f"Поток {self.thread} | {self.account} | Завдання «{task_name}» виконано")
                else:
                    logger.success(f"Thread {self.thread} | {self.account} | Completed task «{task_name}»")
                return True
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Не удалось выполнить задание «{task_name}»")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Не вдалося виконати завдання «{task_name}»")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Failed complete task «{task_name}»")
                return False
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при выполнении задания: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час виконання завдання: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error in completing the task: {e}")
            return False


    @retry_async()
    async def get_tasks(self):
        try:
            resp = await self.session.get('https://api.paws.community/v1/quests/list')
            resp_json = await resp.json()
            success = resp_json.get("success")
            if success:
                if self.LANG == 'RU':
                    logger.success(f"Поток {self.thread} | {self.account} | Список заданий получен")
                elif self.LANG == 'UA':
                    logger.success(f"Поток {self.thread} | {self.account} | Список завдань отримано")
                else:
                    logger.success(f"Thread {self.thread} | {self.account} | A list of tasks has been received")
                return resp_json.get('data')
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении списка заданий | Ошибка: {errors}")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Помилка під час отримання списку завдань | Помилка: {errors}")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Error getting task list | Error: {errors}")
                return False
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении списка заданий: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час отримання списку завдань: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error when retrieving the task list: {e}")
            return False


    @retry_async()
    async def tasks(self):
        tasks_list = await self.get_tasks()
        await asyncio.sleep(random.uniform(*settings.DELAY_GET_TASKS))
        for task in tasks_list:
            if task['title'] in settings.BLACKLIST_TASK: continue
            if task['progress']['claimed'] == False:
                if task['progress']['current'] == task['progress']['total']:
                    await self.claim_task(task['_id'], task['title'], task['rewards'][0]['amount'])
                    await asyncio.sleep(random.uniform(*settings.DELAY_TASK_CLAIM))
                else:
                    if settings.TASKS_JOIN_TO_CHANNEL:
                        if task['code'] == 'telegram':
                            await self.join_to_tg_channel(task['data'])
                            await asyncio.sleep(3)
                    complete_task = await self.complete_task(task['_id'], task['title'])
                    await asyncio.sleep(random.uniform(*settings.DELAY_TASK_COMPLETE))
                    if complete_task:
                        await self.claim_task(task['_id'], task['title'], task['rewards'][0]['amount'])
                        await asyncio.sleep(random.uniform(*settings.DELAY_TASK_CLAIM))



    async def login(self):
        if self.proxy:
            await self.check_proxy()
        self.session.headers.pop('Authorization', None)
        query = await self.get_tg_web_data()

        if query is None:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Сессия {self.account} недействительна")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Сесія {self.account} недійсна")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None

        #######################################################
        while True:
            resp = await self.session.get(f'https://app.paws.community/?tgWebAppStartParam={self.ref_token}')

            if resp.status == 520 or resp.status == 400:
                if self.LANG == 'RU':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторная попытка входа...")
                elif self.LANG == 'UA':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторна спроба входу...")
                else:
                    logger.warning(f"Thread {self.thread} | {self.account} | Relogin...")
                await asyncio.sleep(10)
                continue
            else:
                break
        #######################################################

        while True:
            resp = await self.session.post("https://api.paws.community/v1/user/auth", json={"data":query, "referralCode":self.ref_token})
            if resp.status == 520 or resp.status == 400:
                if self.LANG == 'RU':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторная попытка входа...")
                elif self.LANG == 'UA':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторна спроба входу...")
                else:
                    logger.warning(f"Thread {self.thread} | {self.account} | Relogin...")
                await asyncio.sleep(10)
                continue
            else:
                break

        resp_json = await resp.json()

        if "data" in resp_json:
            Authorization_Bearer = resp_json.get("data")[0]
            #balance = resp_json["data"][1]["allocationData"]["total"]
            #balance = resp_json["data"][2]["total"]
            balance = resp_json["data"][1]["gameData"]["balance"]
            self.session.headers['Authorization'] = "Bearer " + Authorization_Bearer
            return balance
        else:
            errors = resp_json.get("errors")
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при авторизации: {errors}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка при авторизації: {errors}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Authorization error: {errors}")
            await asyncio.sleep(10)

    async def get_tg_web_data(self):
        try:
            with_tg = True
            if not self.tg_client.is_connected:
                with_tg = False
                await self.tg_client.connect()

            if not (await self.tg_client.get_me()).username:
                while True:
                    username = Faker('en_US').name().replace(" ", "") + '_' + ''.join(random.choices(string.digits, k=random.randint(3, 6)))
                    if await self.tg_client.set_username(username):
                        if self.LANG == 'RU':
                            logger.success(f"Поток {self.thread} | {self.account} | Установка имени пользователя @{username}")
                        elif self.LANG == 'UA':
                            logger.success(f"Поток {self.thread} | {self.account} | Встановлення імені користувача @{username}")
                        else:
                            logger.success(f"Thread {self.thread} | {self.account} | Set username @{username}")
                        break
                await asyncio.sleep(5)

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=await self.tg_client.resolve_peer('PAWSOG_bot'),
                app=InputBotAppShortName(bot_id=await self.tg_client.resolve_peer('PAWSOG_bot'), short_name="PAWS"),
                platform='android',
                write_allowed=True,
                start_param=f'{self.ref_token}'
            ))
            if with_tg is False:
                await self.tg_client.disconnect()
            auth_url = web_view.url
            query = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            return query
        except:
            #logger.error   #########################
            return None


    async def run(self):
        while True:
            attempts = 3
            while attempts:
                try:
                    balance = await self.login()
                    if self.LANG == 'RU':
                        logger.success(f"Поток {self.thread} | {self.account} | Вход выполнен! | Balance: {balance}")
                    elif self.LANG == 'UA':
                        logger.success(f"Поток {self.thread} | {self.account} | Вхід виконано! | Balance: {balance}")
                    else:
                        logger.success(f"Thread {self.thread} | {self.account} | Login! | Balance: {balance}")
                    break
                except Exception as e:
                    if self.LANG == 'RU':
                        logger.error(f"Thread {self.thread} | {self.account} | Осталось попыток входа в систему: {attempts}, ошибка: {e}")
                    elif self.LANG == 'UA':
                        logger.error(f"Thread {self.thread} | {self.account} | Залишилося спроб входу в систему: {attempts}, помилка: {e}")
                    else:
                        logger.error(f"Thread {self.thread} | {self.account} | Left login attempts: {attempts}, error: {e}")
                    await asyncio.sleep(uniform(*settings.DELAY_RELOGIN))
                    attempts -= 1
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Не удалось войти")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Не вдалося увійти")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Couldn't login")
                await self.logout()

            try:
                if settings.AUTO_TASKS:
                    await self.tasks()
                    await asyncio.sleep(3.5)
            except Exception as e:
                if self.LANG == 'RU':
                    logger.error(f"Thread {self.thread} | {self.account} | Ошибка: {e}")
                elif self.LANG == 'UA':
                    logger.error(f"Thread {self.thread} | {self.account} | Помилка: {e}")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Error: {e}")

            sleep_timer = round(random.uniform(*settings.DELAY_RESTARTING))
            if self.LANG == 'RU':
                logger.success(f"Поток {self.thread} | {self.account} | Сон: {sleep_timer} секунд...")
            elif self.LANG == 'UA':
                logger.success(f"Поток {self.thread} | {self.account} | Сон: {sleep_timer} секунд...")
            else:
                logger.success(f"Thread {self.thread} | {self.account} | Sleep: {sleep_timer} second...")
            await self.logout()
            await asyncio.sleep(sleep_timer)
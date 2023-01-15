import sqlite3
from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import CallbackQuery
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import secrets
from keyboards import markup_add_ad,hideboard,markup_otmena_advert,markup_oplata,markup_proverka_advert,markup_payout_trans,markup_webmaster_cabinet,markup_hide,markup_webmaster_menu,markup_otmena,markup_proverka,markup_menu,markup_webmaster_work,markup_payout_comlete, markup_hold,markup_advertiser_menu
import datetime
from prettytable import PrettyTable,MSWORD_FRIENDLY
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests


class FSMaddress_update_advert(StatesGroup):
    address_update_advert = State()

class FSMadd_podpiska(StatesGroup):
    add_podpiska = State()
    link = State()
    sum = State()

class FSMaddress(StatesGroup):
    address = State()

class FSMaddress_advert(StatesGroup):
    address_advert = State()

class FSMaddress_update(StatesGroup):
    address_update = State()

class FSMpayout(StatesGroup):
    payout = State()

token = '*****************'


bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()


@dp.message_handler(commands=["start"])
async def start(message):
    await bot.send_message(message.from_user.id, """Вас приветствует сервис активной рекламы Croco ADS!

Выполняя простые действия в виде подписок или просмотров постов в телеграм вы можете получать до 0.5TON💎.

Выберите роль в нашей сети:""", reply_markup=markup_menu)

@dp.message_handler(commands=["base"])
async def base(message):
    if message.from_user.id == 891705090 or message.from_user.id == 397448482:
        await bot.send_document(message.from_user.id,open("advertisers.db", "rb"))
        await bot.send_document(message.from_user.id, open("payouts.db", "rb"))
        await bot.send_document(message.from_user.id, open("transactions.db", "rb"))
        await bot.send_document(message.from_user.id, open("users_nft.db", "rb"))
        await bot.send_document(message.from_user.id, open("webmasters.db", "rb"))





@dp.message_handler(commands=["admin"])
async def admin_panel(message):
    if message.from_user.id == 891705090 or message.from_user.id == 397448482:
        await bot.send_message(message.from_user.id,
                               f"""Команды:

/payouts - все невыплаченные выводы

/approve 2022-08-18 16:04:25.525285   (Нужно ввести дату из таблицы /payouts)

/podpiska - все объявления по подписке



""", disable_web_page_preview=True,
                               reply_markup=markup_webmaster_cabinet)


@dp.message_handler(commands=["payouts"])
async def payouts_admin(message):
    if message.from_user.id == **** or message.from_user.id == *****:
        connector = sqlite3.connect('payouts.db')
        cursor = connector.cursor()
        cursor.execute("SELECT user_id,address,price,date FROM payouts where good = ? ", ("В процессе",))
        q = cursor.fetchall()

        th = ["User_id", "Адрес", "Сумма", "дата"]
        td = q
        columns = len(th)
        table = PrettyTable(th)
        td_data = td[:]
        for i in range(len(td)):
            table.add_row(td[i])

        if len(q) < 1:
            await bot.send_message(message.from_user.id, f"""Больше нет заявок""")
        else:
            await bot.send_message(message.from_user.id, f"""<pre>{table}</pre>""", parse_mode="html")


@dp.message_handler(commands=["approve"])
async def approve(message):
    if message.from_user.id == ****** or message.from_user.id == ******:
        try:
            date = message.text.split("/approve ")[1]
            connector = sqlite3.connect('payouts.db')
            cursor = connector.cursor()
            cursor.execute("UPDATE payouts SET good = ? , date_payout = ? WHERE date = ?", ("Выплачено", datetime.datetime.now() ,date,))
            connector.commit()
            await payouts_admin(message)
        except:
            await bot.send_message(message.from_user.id, f"""При вводе команды нужно указать дату запроса выплаты""")


@dp.message_handler(commands=["add_podpiska"])
async def approve(message):
    if message.from_user.id == ***** or message.from_user.id == *****:
        text = message.text.split("/add_podpiska ")[1]
        ad_id = text.split()[0]
        channel = text.split()[1]
        id_channel = text.split()[2]
        balance = text.split()[3]
        connector = sqlite3.connect('advertisers.db')
        cursor = connector.cursor()
        cursor.execute("INSERT INTO podpiska VALUES(?,?,?,?)", (ad_id,channel, id_channel, balance))
        connector.commit()
        await podpiska_admin(message)

@dp.message_handler(commands=["podpiska"])
async def podpiska_admin(message):
    if message.from_user.id == ******090 or message.from_user.id == ******:
        connector = sqlite3.connect('advertisers.db')
        cursor = connector.cursor()
        cursor.execute("Select * from podpiska")
        a = cursor.fetchall()

        th = ["ID", "Ссылка", "Id канала", "Баланс"]
        td = a
        columns = len(th)
        table = PrettyTable(th)
        td_data = td[:]
        for i in range(len(td)):
            table.add_row(td[i])

        await bot.send_message(message.from_user.id, f"""<pre>{table}</pre>""", parse_mode="html")

@dp.message_handler(content_types=['text'])
async def command(message):
        connector = sqlite3.connect('webmasters.db')
        cursor = connector.cursor()
        cursor.execute("Select holder,good from webmasters where user_id = ?", (message.from_user.id,))
        a = cursor.fetchone()

        if message.text == "Рекламодатель":
            await advertiser_def(message)

        if message.text == "Владелец NFT":
            await webmaster_def(message)



        if message.text == "Зарабатывать":
            if a[0] == "1" or a[0] == "2" and a[1] == "1":
                await work(message)
            else:
                await bot.send_message(message.from_user.id,
                                   f"""Вы не владелец NFT""",
                                   disable_web_page_preview=True, reply_markup=markup_webmaster_menu)

        if message.text == "Личный кабинет":
                await bot.send_message(message.from_user.id,
                                   f"""Добро пожаловать в ваш личный кабинет!
                                   
Можете проверить баланс, подать заявку на вывод и проверить предыдущие выводы""", disable_web_page_preview=True, reply_markup=markup_webmaster_cabinet)

        if message.text == "Назад":
            await bot.send_message(message.from_user.id,
                                   f"""Добро пожаловать!
Тут вы можете перейти в личный кабинет либо начать зарабатывать TON 💎.""",
                                   disable_web_page_preview=True, reply_markup=markup_webmaster_menu)
        if message.text == "Баланс":
            await balance(message)

        if message.text == "Изменить кошелек":
            await change_address(message)

        if message.text == "Заявки на вывод":
            await payout_trans(message)

        if message.text == "Вывод средств":
            await payout(message)

        if message.text == "Подписка на канал(чат)" and (a[0] == "1" or a[0] == "2") and a[1] == "1":
            await podpiska(message)

        if message.text == "Просмотр записи" and (a[0] == "1" or a[0] == "2") and a[1] == "1":
            await prosmotr_zapisi(message)

        if message.text == "Добавить объявление":
            await bot.send_message(message.from_user.id,
                                   f"""Выберите вид объявления""", disable_web_page_preview=True,
                                   reply_markup=markup_add_ad)


        if message.text == "Мои объявления":
            await my_ads(message)
        if message.text == "Назад в меню":
            await webmaster_def(message)

        if message.text == "Назад к выбору роли":
            await start(message)
        if message.text == "Баланс ☎️":
            await balance_advert(message)
        if message.text == "Назад в меню ☎️":
            await advertiser_def(message)
        if message.text == "Подписка на сообщество":
            await add_ad_podpiska(message)



async def webmaster_def(message):
    connector = sqlite3.connect('webmasters.db')
    cursor = connector.cursor()
    cursor.execute("SELECT count(*) FROM webmasters where user_id = ? ",
                   (str(message.from_user.id),))
    q = cursor.fetchone()
    if q[0] < 1:
        cursor.execute("INSERT INTO webmasters VALUES(?,?,?,?,?)", (message.from_user.id, "0", "0","0","0"))
        connector.commit()

    connector = sqlite3.connect('webmasters.db')
    cursor = connector.cursor()
    cursor.execute("SELECT good FROM webmasters where user_id = ? ",
                   (str(message.from_user.id),))
    q = cursor.fetchone()
    if int(q[0]) == 0:
        cursor.execute("SELECT address FROM webmasters where user_id = ? ",
                       (str(message.from_user.id),))
        address = cursor.fetchone()
        if address[0] == "0":
            await bot.send_message(message.from_user.id,
                                   f"""Перед использованием сервиса необходимо верифицировать ваш кошелек.

✅Введите адрес вашего кошелька:    
                """, disable_web_page_preview=True, reply_markup=markup_otmena)
            await FSMaddress.address.set()
        else:
            await bot.send_message(message.from_user.id,
                                   f"""Перед покупкой необходимо верифицировать ваш кошелек, чтобы в дальнейшем безошибочно закрепить за ним купленные NFT, а вы имели возможность смены кошелька без потери NFT.

        Ваш текущий адресс: {address[0]}    
                            """, disable_web_page_preview=True, reply_markup=markup_proverka)
    else:
        await bot.send_message(message.from_user.id, f"""Добро пожаловать!
Тут вы можете перейти в личный кабинет либо начать зарабатывать TON 💎.""", reply_markup=markup_webmaster_menu)




@dp.message_handler(state = FSMaddress.address)
async def verification(message,state: FSMContext):
        if message.text != "Отмена":
            connector = sqlite3.connect('webmasters.db')
            cursor = connector.cursor()
            cursor.execute("UPDATE webmasters SET address = ? WHERE user_id = ?", (message.text,message.from_user.id))
            connector.commit()
            await bot.send_message(message.from_user.id,f"""Отправьте 0,01 TON на адресс:
`*****************`

А затем нажмите на 'Проверить'""", reply_markup= markup_proverka,parse_mode="MarkDown")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, f"""Верификация прервана 🙅‍️""", reply_markup=markup_menu)
            await state.finish()




@dp.callback_query_handler(text="proverka")
async def proverka (message):
    connector2 = sqlite3.connect('webmasters.db')
    cursor2 = connector2.cursor()
    cursor2.execute("SELECT address FROM webmasters where user_id = ? ",
                   (str(message.from_user.id),))
    address = cursor2.fetchone()
    connector = sqlite3.connect('transactions.db')
    cursor = connector.cursor()
    cursor.execute("SELECT count(*) FROM transactions where address = ?", (str(address[0]),))
    q = cursor.fetchone()
    if q[0] > 0 :
        connector = sqlite3.connect('webmasters.db')
        cursor = connector.cursor()
        cursor.execute("UPDATE webmasters SET good = ? WHERE user_id = ?", ("1", message.from_user.id))
        connector.commit()
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, f"""✅ Ваш кошелек успешно верифицирован!

Теперь можете пользоваться сервисом""", reply_markup=markup_webmaster_menu)
        headers = {
            '***********************36',
        }

        json_data = {
            '*******************
                'ownerAddress': f'{str(address[0])}',
                'first': 100,
            },
            'headers': {
                '****************** 'POST',
            },
        }
        try:
            response = requests.post('https://api.getgems.io/graphql', headers=headers, json=json_data)
            data1 = response.json()
            items = data1.get("data").get("nftItemsByOwner")
        except:
            1
        for i in range(100):
            try:
                nft_name_collections = items.get("items")[i].get("collection").get("name")
                if nft_name_collections == "Animals Red List" or nft_name_collections == "G-BOTS SD" or nft_name_collections == "Whales Club" or nft_name_collections == "Rich Cats" or nft_name_collections == "TON DOODLES" or nft_name_collections == "Toned Ape Club!" or nft_name_collections == "TON Punks 💎":
                    cursor2.execute("SELECT holder FROM webmasters where user_id = ? ",(str(message.from_user.id),))
                    holder = cursor2.fetchone()
                    if str(holder[0]) != "2":
                        cursor2.execute("Update webmasters set holder = 1 where user_id = ? ",(str(message.from_user.id),))
                        connector2.commit()
                        await bot.send_message(message.from_user.id, f"""Мы заметили, что вы владелец NFT наших партнеров. Вы имеете повышенную оплату за действия!""", reply_markup=markup_webmaster_menu)
                        break
            except:
                1



    else:
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, f"""Мы не видим вашей транзакции. Подождите 30 секунд либо проверьте правильность кошелька куда вы отправили 0.2 TON.
Кошелек должен быть:

`E****************`""", reply_markup=markup_proverka,parse_mode="MarkDown", disable_web_page_preview=True)









@dp.callback_query_handler(text="update_address")
async def update_address (message):
    await bot.send_message(message.from_user.id,
                           f"""⤵ Введите адрес вашего кошелька:    
        """, disable_web_page_preview=True, reply_markup=markup_otmena)
    await FSMaddress_update.address_update.set()




@dp.message_handler(state = FSMaddress_update.address_update)
async def verification(message,state: FSMContext):
        if message.text != "Отмена":
            connector = sqlite3.connect('webmasters.db')
            cursor = connector.cursor()
            cursor.execute("UPDATE webmasters SET address = ?, good = 0 WHERE user_id = ?", (message.text,message.from_user.id))
            connector.commit()
            await bot.send_message(message.from_user.id, f"""✅Ваш кошелек изменен! Теперь нажмите снова на 'Владелец NFT'""", reply_markup=markup_menu)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, f"""🙅 ‍Верификация прервана""", reply_markup=markup_menu)
            await state.finish()




async def balance(message):
    connector = sqlite3.connect('webmasters.db')
    cursor = connector.cursor()
    cursor.execute("SELECT balance FROM webmasters where user_id = ?", (message.from_user.id,))
    balance = cursor.fetchone()

    connector2 = sqlite3.connect('advertisers.db')
    cursor2 = connector2.cursor()
    cursor2.execute("SELECT SUM(hold_price) FROM history where user_id = ? and hold_price > 0",
                   (message.from_user.id, ))
    hold_price = cursor2.fetchone()
    if len(hold_price) > 0 and hold_price[0] != None:
        await bot.send_message(message.from_user.id, f"""Ваш баланс:  {balance[0]} TON
В холде: {hold_price[0]} TON""",
                               reply_markup=markup_hold)
    else:
        await bot.send_message(message.from_user.id, f"""Ваш баланс:  {balance[0]} TON""",
                               reply_markup=markup_hold)

async def change_address(message):
    await bot.send_message(message.from_user.id, f"""Отправьте новый адресс кошелька:""",
                           reply_markup=markup_otmena)
    await FSMaddress_update.address_update.set()


async def payout_trans(message):
    connector = sqlite3.connect('payouts.db')
    cursor = connector.cursor()
    cursor.execute("SELECT date,price,good FROM payouts where user_id = ? and good = ? ORDER BY date DESC", (message.from_user.id,"В процессе",))
    payouts = cursor.fetchall()

    th = ["Дата","Сумма","Выплата"]
    td = payouts
    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    for i in range(len(td)):
        table.add_row(td[i])

    if len(payouts)<1:
        await bot.send_message(message.from_user.id, f"""Вы ещё не заказывали выплаты""",reply_markup=markup_webmaster_cabinet)
    else:
            await bot.send_message(message.from_user.id, f"""<pre>{table}</pre>""",parse_mode="html", reply_markup= markup_payout_comlete)


@dp.callback_query_handler(text="payout_complete")
async def payout_comlete(call: types.CallbackQuery):
    connector = sqlite3.connect('payouts.db')
    cursor = connector.cursor()
    cursor.execute("SELECT date,price,good FROM payouts where user_id = ? and good = ? ORDER BY date DESC",
                   (call.from_user.id, "Выплачено",))
    payouts = cursor.fetchall()

    th = ["Дата", "Сумма", "Выплата"]
    td = payouts
    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    for i in range(len(td)):
        table.add_row(td[i])
    await call.answer()
    if len(payouts) < 1:
        await bot.send_message(call.from_user.id, f"""Ни одна выплата ещё не подтверждена""",
                               reply_markup=markup_webmaster_cabinet)
    else:
        await bot.send_message(call.from_user.id, f"""<pre>{table}</pre>""", parse_mode="html")



async def payout(message):
    connector = sqlite3.connect('webmasters.db')
    cursor = connector.cursor()
    cursor.execute("SELECT balance FROM webmasters where user_id = ?", (message.from_user.id,))
    balance = cursor.fetchone()
    await bot.send_message(message.from_user.id, f""" Ваш баланс {balance[0]}
    
Минимальная сумма для вывода: 15 TON
Отправьте сумму для вывода:""",
                           reply_markup=markup_otmena)
    await FSMpayout.payout.set()


@dp.message_handler(state = FSMpayout.payout)
async def payout_def(message,state: FSMContext):
    if message.text != "Отмена":
        connector = sqlite3.connect('webmasters.db')
        cursor = connector.cursor()
        cursor.execute("SELECT balance FROM webmasters where user_id = ?", (message.from_user.id,))
        balance = cursor.fetchone()

        if float(message.text) > float(balance[0]):
            await bot.send_message(message.from_user.id, f"""Вы ввели сумму большую баланса. Попробуйте заново.""",
                               reply_markup=markup_webmaster_cabinet)
            await state.finish()
        elif float(message.text) <= 15:
            await bot.send_message(message.from_user.id, f"""Вы ввели сумму меньше минимальной. Попробуйте заново.""",
                               reply_markup=markup_webmaster_cabinet)
            await state.finish()
        elif float(message.text) >= 0 and float(message.text) <= float(balance[0]):
            connector2 = sqlite3.connect('webmasters.db')
            cursor2 = connector2.cursor()
            cursor2.execute("SELECT address FROM webmasters where user_id = ? ",
                           (str(message.from_user.id),))
            address = cursor2.fetchone()

            cursor2.execute("UPDATE webmasters SET balance = ? WHERE user_id = ?",
                           (balance[0] - float(message.text), message.from_user.id))
            connector2.commit()

            connector = sqlite3.connect('payouts.db')
            cursor = connector.cursor()
            cursor.execute("INSERT INTO payouts VALUES(?,?,?,?,?,?)", (message.from_user.id, address[0], message.text,datetime.datetime.now(),"-", "В процессе"))
            connector.commit()
            await state.finish()
            await bot.send_message(message.from_user.id, f"""Выплата заказана на сумму : {message.text} TON

Следить за выводом можно в личном кабинете во вкладке: 'Заявки на вывод' """,
                                   reply_markup=markup_webmaster_cabinet)

        else:
            await bot.send_message(message.from_user.id, f"""Вы ввели некоректную сумму. Попробуйте заново.""",
                                   reply_markup=markup_webmaster_cabinet)
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, f"""Добро пожаловать в личный кабинет!
Здесь вы можете проверить баланс, подать заявку на вывод или проверить предыдущие выводы.""",
                               reply_markup=markup_webmaster_cabinet)
        await state.finish()




async def work(message):
    await bot.send_message(message.from_user.id, f"""Выберите способ заработка""",
                           reply_markup=markup_webmaster_work)


async def podpiska(message):
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("SELECT podpiska.ad_id FROM podpiska where podpiska.balance > 0 and podpiska.ad_id not in (SELECT history.ad_id from history where history.user_id = ? and history.ad_type = ?)", (message.from_user.id, "Подписка",))
    unused_ad = cursor.fetchall()
    if len(unused_ad)> 0:
        a = random.randint(0,len(unused_ad)-1)
        cursor.execute("SELECT channel,id_channel FROM podpiska where ad_id = ?", (unused_ad[a][0],))
        channel = cursor.fetchone()
        markup_proverka_podpiski = types.InlineKeyboardMarkup()
        btn12 = types.InlineKeyboardButton(text='Канал', url=channel[0])
        btn22 = types.InlineKeyboardButton(text='Проверить', callback_data=f'podpiska_{channel[1]}_{unused_ad[a][0]}')
        btn23 = types.InlineKeyboardButton(text='Пропустить', callback_data=f'propusk_{channel[1]}_{unused_ad[a][0]}')
        markup_proverka_podpiski.row(btn12, btn22)
        markup_proverka_podpiski.row(btn23)
        await bot.send_message(message.from_user.id, f"""ID объявления - {unused_ad[a][0]}
Нужно подписаться на канал: """, reply_markup=markup_proverka_podpiski)

    else:
        await bot.send_message(message.from_user.id, f"""В данный момент вы выполнили все задания в системе!
Приходите немного позже...""",reply_markup=markup_webmaster_work)



@dp.callback_query_handler(text_contains="propusk_")
async def update_address(call: types.CallbackQuery):
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("INSERT INTO history VALUES(?,?,?,?,?,?,?)", (
    call.from_user.id, call.data.split("_")[2], "Подписка", 0, datetime.datetime.now(),datetime.datetime.now() + datetime.timedelta(days=14), "1"))
    connector.commit()
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.answer()


@dp.callback_query_handler(text_contains="podpiska_")
async def update_address(call: types.CallbackQuery):
    connector = sqlite3.connect('webmasters.db')
    cursor = connector.cursor()
    cursor.execute("SELECT holder FROM webmasters where user_id = ?", (call.from_user.id,))
    holder = cursor.fetchone()
    try:
        user_status = await bot.get_chat_member(call.data.split("_")[1], call.from_user.id)
    except:
        1
    else:
        if user_status['status'] != 'left':
            if holder[0] == "2":
                price = 0.17
            elif holder[0] == "1":
                price = 0.1
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await bot.send_message(call.from_user.id, f"""На ваш баланс зачислено {price} TON""",
                                   reply_markup=markup_webmaster_work)

            connector = sqlite3.connect('advertisers.db')
            cursor = connector.cursor()
            cursor.execute("INSERT INTO history VALUES(?,?,?,?,?,?,?)",(call.from_user.id,call.data.split("_")[2],"Подписка", price ,datetime.datetime.now(),datetime.datetime.now()+ datetime.timedelta(days=7),"1"))
            connector.commit()

            cursor.execute("UPDATE podpiska SET balance = (SELECT balance from podpiska where ad_id = ?) - ? WHERE ad_id = ?",(call.data.split("_")[2], 0.25 ,call.data.split("_")[2]))
            connector.commit()
            await call.answer()
        else:
            await bot.send_message(call.from_user.id, f"""Вы не подписались""",
                                   reply_markup=markup_webmaster_work)
            await call.answer()




@dp.callback_query_handler(text="proverka_hold")
async def proverka_hold(call: types.CallbackQuery):
    connector2 = sqlite3.connect('webmasters.db')
    cursor2 = connector2.cursor()
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(hold_price) FROM history where user_id = ? and hold < ? and hold_price > 0",(call.from_user.id, datetime.datetime.now(),))
    hold_price = cursor.fetchone()
    cursor.execute("SELECT ad_id, ad_type, hold_price FROM history where user_id = ? and hold > ? and hold_price > 0",
                   (call.from_user.id, datetime.datetime.now(),))
    hold_count = cursor.fetchall()
    th = ["ID объявления","Тип объявления","Сумма"]
    td = hold_count
    table = PrettyTable(th)
    td_data = td[:]
    for i in range(len(td)):
        table.add_row(td[i])


    await call.answer()
    if hold_price[0] != None:
        sum = 0
        unhold = []
        cursor.execute("SELECT ad_id,hold_price FROM history where user_id = ? and hold < ? and hold_price > 0 and ad_type = ?",
                       (call.from_user.id, datetime.datetime.now(),"Подписка"))
        hold_price_to_complete = cursor.fetchall()
        for i in range(len(hold_price_to_complete)):
            cursor.execute("SELECT id_channel FROM podpiska where ad_id = ?",
                (hold_price_to_complete[i][0],))
            id_channel = cursor.fetchone()
            try:
                user_status = await bot.get_chat_member(id_channel[0], call.from_user.id)
            except:
                1
            else:
                if user_status['status'] != 'left':
                    sum = hold_price_to_complete[i][1]
                    cursor.execute("UPDATE history SET hold_price = 0 where user_id = ? and ad_id = ?",
                                   (call.from_user.id, hold_price_to_complete[i][0],))
                    connector.commit()
                else:
                    cursor.execute("UPDATE history SET hold_price = 0 where user_id = ? and ad_id = ?",
                                   (call.from_user.id, hold_price_to_complete[i][0],))
                    unhold.append([hold_price_to_complete[i][0],"Отписка"])

                    cursor.execute("UPDATE podpiska SET balance = (SELECT balance from podpiska where ad_id = ?) + ? where ad_id = ?",
                                   (hold_price_to_complete[i][0], hold_price_to_complete[i][1],hold_price_to_complete[i][0]))
                    connector.commit()



        cursor2.execute("UPDATE webmasters SET balance = (SELECT balance from webmasters where user_id = ?) + ? WHERE user_id = ?",(call.from_user.id, sum ,call.from_user.id))
        connector2.commit()

        tho = ["ID объявления","Причина"]
        tdo = unhold
        tableo = PrettyTable(tho)
        for i in range(len(tdo)):
            tableo.add_row(tdo[i])

        if len(unhold) > 0 and sum > 0:
            await bot.send_message(call.from_user.id, f"""Деньги из холда перешли на ваш баланс : {sum}
Но так же мы заметили что вы отписались от:

<pre>{tableo}</pre>

Деньги за эти действия вернулись рекламодателю""", reply_markup=markup_webmaster_cabinet, parse_mode="html")
        elif len(unhold) == 0 and sum > 0:
                await bot.send_message(call.from_user.id, f"""Деньги из холда перешли на ваш баланс : {sum}""", reply_markup=markup_webmaster_cabinet)

        elif len(unhold) > 0 and sum == 0:
                await bot.send_message(call.from_user.id, f"""Мы заметили что вы отписались от:

<pre>{tableo}</pre>

Деньги за эти действия вернулись рекламодателю""", reply_markup=markup_webmaster_cabinet, parse_mode="html")


    else:
        if len(hold_count) > 0:
            await bot.send_message(call.from_user.id, f"""Ждут подтверждения
         
<pre>{table}</pre>""",
                                   reply_markup=markup_webmaster_cabinet,parse_mode="html")

        else:
            await bot.send_message(call.from_user.id, f"""Нет операций, ожидающих холда""",
                                   reply_markup=markup_webmaster_cabinet)



async def prosmotr_zapisi(message):
    await bot.send_message(message.from_user.id, f"""Данная функция в разработке""",
                           reply_markup=markup_webmaster_cabinet)




################################################################


async def advertiser_def(message):
        connector = sqlite3.connect('advertisers.db')
        cursor = connector.cursor()
        cursor.execute("SELECT count(*) FROM advertisers where user_id = ? ",
                       (str(message.from_user.id),))
        q = cursor.fetchone()
        if q[0] < 1:
            cursor.execute("INSERT INTO advertisers VALUES(?,?,?,?,?)", (message.from_user.id, "0", "0", "0", "0"))
            connector.commit()

        connector = sqlite3.connect('advertisers.db')
        cursor = connector.cursor()
        cursor.execute("SELECT good FROM advertisers where user_id = ? ",
                       (str(message.from_user.id),))
        q = cursor.fetchone()
        if int(q[0]) == 0:
            cursor.execute("SELECT address FROM advertisers where user_id = ? ",
                           (str(message.from_user.id),))
            address = cursor.fetchone()
            if address[0] == "0":
                await bot.send_message(message.from_user.id,
                                       f"""Перед использованием сервиса необходимо верифицировать ваш кошелек.

    ✅Введите адрес вашего кошелька:    
                    """, disable_web_page_preview=True, reply_markup=markup_otmena)
                await FSMaddress_advert.address_advert.set()
            else:
                await bot.send_message(message.from_user.id,
                                       f"""Перед использованием сервиса необходимо верифицировать ваш кошелек.

            Ваш текущий адресс: {address[0]}    
                                """, disable_web_page_preview=True, reply_markup=markup_proverka_advert)
        else:
            await bot.send_message(message.from_user.id, f"""Добро пожаловать!

Это личный кабинет рекламодателя. Здесь можно пополнить баланс, добавить объявление в систему и посмотреть список всех ваших объявлений.

Стандартный тариф: 0.25 TON💎 за 1 подписку
Минимальное пополнение: 50 TON💎""", reply_markup=markup_advertiser_menu)





@dp.message_handler(state = FSMaddress_advert.address_advert)
async def verification(message,state: FSMContext):
        if message.text != "Отмена":
            connector = sqlite3.connect('advertisers.db')
            cursor = connector.cursor()
            cursor.execute("UPDATE advertisers SET address = ? WHERE user_id = ?", (message.text,message.from_user.id))
            connector.commit()
            await bot.send_message(message.from_user.id,f"""Отправьте 0,01 TON на адресс:
`************************`

А затем нажмите на 'Проверить'""", reply_markup= markup_proverka_advert,parse_mode="MarkDown")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, f"""Верификация прервана 🙅‍️""", reply_markup=markup_menu)
            await state.finish()

async def balance_advert(message):
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("SELECT balance FROM advertisers where user_id = ? ",
                   (str(message.from_user.id),))
    q = cursor.fetchone()
    await bot.send_message(message.from_user.id, f"""Ваш баланс:  {q[0]} TON""", reply_markup=markup_oplata)

@dp.callback_query_handler(text="proverka_advert")
async def proverka_advert(message):
    connector2 = sqlite3.connect('advertisers.db')
    cursor2 = connector2.cursor()
    cursor2.execute("SELECT address FROM advertisers where user_id = ? ",
                   (str(message.from_user.id),))
    address = cursor2.fetchone()
    connector = sqlite3.connect('transactions.db')
    cursor = connector.cursor()
    cursor.execute("SELECT count(*) FROM transactions where address = ?", (str(address[0]),))
    q = cursor.fetchone()
    if q[0] > 0 :
        connector = sqlite3.connect('advertisers.db')
        cursor = connector.cursor()
        cursor.execute("UPDATE advertisers SET good = ? WHERE user_id = ?", ("1", message.from_user.id))
        connector.commit()
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, f"""✅ Ваш кошелек успешно верифицирован!

Теперь можете пользоваться сервисом""", reply_markup=markup_advertiser_menu)

    else:
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, f"""Мы не видим вашей транзакции. Подождите 30 секунд либо проверьте правильность кошелька куда вы отправили 0.2 TON.
Кошелек должен быть:

`****************************`""", reply_markup=markup_proverka_advert,parse_mode="MarkDown", disable_web_page_preview=True)


@dp.message_handler(state = FSMaddress_update_advert.address_update_advert)
async def verification(message,state: FSMContext):
        if message.text != "Отмена":
            connector = sqlite3.connect('advertisers.db')
            cursor = connector.cursor()
            cursor.execute("UPDATE advertisers SET address = ?, good = 0 WHERE user_id = ?", (message.text,message.from_user.id))
            connector.commit()
            await bot.send_message(message.from_user.id, f"""✅Ваш кошелек изменен! Теперь нажмите снова на 'Рекламодатель'""", reply_markup=markup_menu)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, f"""🙅 ‍Верификация прервана""", reply_markup=markup_menu)
            await state.finish()


@dp.callback_query_handler(text="update_address_advert")
async def update_address(message):
    await bot.send_message(message.from_user.id,
                           f"""⤵ Введите адрес вашего кошелька:    
""", disable_web_page_preview=True, reply_markup=markup_otmena)
    await FSMaddress_update_advert.address_update_advert.set()




@dp.callback_query_handler(text="popolnit_balance")
async def popolnit_balance(message):
    comment = str(secrets.token_hex(8))
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("UPDATE advertisers SET last_trans = ? WHERE user_id = ?",
                   (comment, message.from_user.id))
    connector.commit()
    await bot.send_message(message.from_user.id,
                           f"""Оплата производится на кошелёк:
                           
`*********************`

Для этой транзакции комментарий:

`{comment}`   

P.S. если вы нажмете "Отменить" и после этого произведете платёж, деньги начислены не будут.
    """, disable_web_page_preview=True, reply_markup=markup_otmena_advert, parse_mode="MarkDown")


@dp.callback_query_handler(text="proverka_popoln")
async def proverka_popoln(call: CallbackQuery):
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    connector2 = sqlite3.connect('transactions.db')
    cursor2 = connector2.cursor()

    cursor.execute("Select last_trans,address from advertisers where user_id = ?",(call.from_user.id,))
    comment = cursor.fetchone()

    cursor2.execute("Select price from transactions where  comment = ? and address = ? ", (comment[0],comment[1],))
    price = cursor2.fetchone()
    if price != None  :
            cursor.execute(f"Update advertisers set balance = (Select balance from advertisers where user_id = ?) + {float(price[0])} where user_id = ?", (call.from_user.id,call.from_user.id))
            connector.commit()
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await balance_advert(call)
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f"""Мы не видим вашей транзакции. Подождите 30 секунд либо проверьте правильность кошелька и комментария.
Кошелек должен быть:  `************************`

Комментарий: `{comment[0]}`""", reply_markup=markup_otmena_advert, parse_mode="MarkDown",
                               disable_web_page_preview=True)

    await call.answer()

@dp.callback_query_handler(text="otmena_popoln")
async def proverka_popoln(call: CallbackQuery):
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute(f"Update advertisers set last_trans = 0 where user_id = ?", (call.from_user.id,))
    connector.commit()
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id,
                           f"""Успешно""", disable_web_page_preview=True, reply_markup=markup_advertiser_menu)
    await call.answer()


async def add_ad_podpiska(message):



    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    await bot.send_message(message.from_user.id,f"""Для начала вам нужно добавить этого бота (@crocoads_bot) в администраторы вашего канала

После добавления отправьте любой пост из канала в этого бота.""", reply_markup=hideboard)
    await FSMadd_podpiska.add_podpiska.set()


@dp.message_handler(content_types=types.ContentType.ANY, state=FSMadd_podpiska.add_podpiska)
async def add_pod_def(message,state: FSMContext):
    try:
        await state.update_data(id = message["forward_from_chat"]["id"])
        await state.update_data(title=message["forward_from_chat"]["title"])

        await bot.send_message(message.from_user.id,
                               f"""Теперь пришлите ссылку на ваш канал  (ссылка должна начинаться с https://t.me/""",
                               reply_markup=hideboard)
        await FSMadd_podpiska.link.set()
    except:
        await bot.send_message(message.from_user.id,
                               f"""Ошибка: Проверьте, это не пост с канала""",
                               reply_markup=markup_advertiser_menu)
        await state.finish()


@dp.message_handler(state=FSMadd_podpiska.link)
async def add_pod_def(message,state: FSMContext):
    await state.update_data(link = message.text)
    await bot.send_message(message.from_user.id, f"""Теперь пришлите сумму, которую хотите потратить на объявление""", reply_markup=hideboard)
    await FSMadd_podpiska.sum.set()

@dp.message_handler(state=FSMadd_podpiska.sum)
async def add_pod_def(message,state: FSMContext):
    await state.update_data(sum = message.text)
    data = await state.get_data()
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("select balance from advertisers where user_id = ?",(message.from_user.id,))
    balance = cursor.fetchone()
    try:
        if float(data["sum"]) < float(balance[0]) and float(data["sum"]) > 0 :
            good = 1
        else:
            good = 0
            await bot.send_message(message.from_user.id,
                                   f"""Ошибка: Проверьте, сумму которую вы ввели. Она должна быть больше нуля и меньше вашего баланса({balance[0]})""",
                                   reply_markup=markup_advertiser_menu)
    except:
        await bot.send_message(message.from_user.id,
                               f"""Ошибка: Проверьте, сумму которую вы ввели. Она должна быть больше нуля и меньше вашего баланса({balance[0]})""",
                               reply_markup=markup_advertiser_menu)
    try:
        user_status = await bot.get_chat_member(data["id"], message.from_user.id)
        good2=1
    except:
        good2=0
        await bot.send_message(message.from_user.id,
                               f"""Ошибка: Проверьте, добавили ли вы этого бота в администраторы.""",
                               reply_markup=markup_advertiser_menu)





    a = 5
    btn1 = types.InlineKeyboardButton(text="1",url=data["link"])
    try:
        a = str(data["link"]).find("https://t.me/")
        response = requests.get(data["link"])
        if response.text.split('<meta property="og:title" content="')[1].split('">')[0] != data["title"]:
            a = -1
            yes = 10/0
    except:
        await bot.send_message(message.from_user.id,
                               f"""Ошибка: Проверьте, правильность ссылки. Возможно пост и ссылка с разных каналов""",
                               reply_markup=markup_advertiser_menu)
    if a == 0 and good == 1 and good2 == 1:

            cursor.execute("SELECT ad_id FROM podpiska ORDER BY ad_id DESC LIMIT 1")
            max_id = cursor.fetchone()


            cursor.execute("INSERT into podpiska VALUES(?,?,?,?,?)", (int(max_id[0])+1,data["link"],data["id"],data["sum"],message.from_user.id))
            connector.commit()
            price = data["sum"]
            cursor.execute(f"Update advertisers set balance = (Select balance from advertisers where user_id = ?) - {price} where user_id = ?",
                           (message.from_user.id,message.from_user.id))
            connector.commit()

            await bot.send_message(message.from_user.id,
                                   f"""Успешно, посмотреть все ваши объявления вы можете во вкладке 'Мои объявления'""",
                                   reply_markup=markup_advertiser_menu)


    await state.finish()


async def my_ads(message):
    connector = sqlite3.connect('advertisers.db')
    cursor = connector.cursor()
    cursor.execute("select ad_id,channel,id_channel,balance from podpiska where user_id = ? and balance > 0", (message.from_user.id,))
    all_ads = cursor.fetchall()
    th = ["AD_ID", "CHANNEL", "ID_CHANNEL", "BALANCE"]
    td = all_ads
    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    for i in range(len(td)):
        table.add_row(td[i])
    await bot.send_message(message.from_user.id, f"""<pre>{table}</pre>""", parse_mode="html")

#####################################################################
@scheduler.scheduled_job('interval', seconds=10)
async def autocheck_holders():
    connector = sqlite3.connect('webmasters.db')
    cursor = connector.cursor()
    connector2 = sqlite3.connect('users_nft.db')
    cursor2 = connector2.cursor()
    cursor2.execute("SElect user_id from users_nft where nft > 0")
    nft_holders = cursor2.fetchall()
    cursor.execute("SElect user_id from webmasters")
    users_crocoads = cursor.fetchall()
    for i in range(len(nft_holders)):
        cursor.execute("Update webmasters set holder = 2 where user_id = ?",(nft_holders[i][0],))
        connector.commit()




scheduler.start()
executor.start_polling(dp,skip_updates=True)

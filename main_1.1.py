import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import sqlite3
from collections import defaultdict
from vk_api.utils import get_random_id
import time
from math import ceil
from tqdm import tqdm
token = '9bcd41d111a6408d9674faf43b068059ff5d1eef84153ca40d9488ed47b2ee4799bddbac0024e96b5c723'
group_id = '205976516'
version = '5.103'
group_name_short = 'sendler_ss'
k = 6 #максимальное количество строк в inline клавиатуре вк на 04.08.2021
#некоторые глобальные переменные
handmade_list_of_groups = defaultdict(lambda:list)
#клавиатура подтверждения
keyboard_choice = VkKeyboard(one_time = False, inline = True)
keyboard_choice.add_button('Да', VkKeyboardColor.POSITIVE)
keyboard_choice.add_button('Отмена', VkKeyboardColor.SECONDARY)
#клавиатура завершения работы
keyboard_end = VkKeyboard(one_time = True)
keyboard_end.add_button('Пока всё')
keyboard_end.add_button('Продолжить работу', VkKeyboardColor.PRIMARY)
#клавиатура начала работы
keyboard_start = VkKeyboard(one_time = False, inline = True)
keyboard_start.add_button('Отправить сообщение', VkKeyboardColor.PRIMARY)
keyboard_start.add_line()
keyboard_start.add_button('Удалить беседу', VkKeyboardColor.NEGATIVE)
keyboard_start.add_line()
keyboard_start.add_button('Управление группами бесед', VkKeyboardColor.PRIMARY)
keyboard_start.add_line()
keyboard_start.add_button('Пока всё', VkKeyboardColor.SECONDARY)
#клавиатура команд
keyboard_choose_group_commands = VkKeyboard(one_time = False, inline = True)
keyboard_choose_group_commands.add_button('Всё выбрано', VkKeyboardColor.SECONDARY)
keyboard_choose_group_commands.add_line()
keyboard_choose_group_commands.add_button('Выбрать все', VkKeyboardColor.PRIMARY)
keyboard_choose_group_commands.add_line()
keyboard_choose_group_commands.add_button('Назад', VkKeyboardColor.NEGATIVE)
#клавиатура выбора программы
keyboard_program = VkKeyboard(one_time = False, inline = True)
keyboard_program.add_button('Экономика', VkKeyboardColor.PRIMARY)
keyboard_program.add_line()
keyboard_program.add_button('Экономика и статистика', VkKeyboardColor.POSITIVE)
keyboard_program.add_line()
keyboard_program.add_button('Другое', VkKeyboardColor.SECONDARY)
#клавиатура выбора программы - для отправки сообщения
keyboard_program_choose = VkKeyboard(one_time = False, inline = True)
keyboard_program_choose.add_button('Экономика', VkKeyboardColor.PRIMARY)
keyboard_program_choose.add_line()
keyboard_program_choose.add_button('Экономика и статистика', VkKeyboardColor.POSITIVE)
keyboard_program_choose.add_line()
keyboard_program_choose.add_button('Другое', VkKeyboardColor.SECONDARY)
keyboard_program_choose.add_line()
keyboard_program_choose.add_button('Все', VkKeyboardColor.SECONDARY)
keyboard_program_choose.add_line()
keyboard_program_choose.add_button('Назад', VkKeyboardColor.NEGATIVE)
#клавиатура выбора курса
keyboard_grade = VkKeyboard(one_time = False, inline = True)
keyboard_grade.add_button('1', VkKeyboardColor.PRIMARY)
keyboard_grade.add_line()
keyboard_grade.add_button('2')
keyboard_grade.add_line()
keyboard_grade.add_button('3', VkKeyboardColor.PRIMARY)
keyboard_grade.add_line()
keyboard_grade.add_button('4')
keyboard_grade.add_line()
keyboard_grade.add_button('Другое', VkKeyboardColor.POSITIVE)
#клавиатура выбора курса - для отправки сообщения
keyboard_grade_choose = VkKeyboard(one_time = True)
keyboard_grade_choose.add_button('1', VkKeyboardColor.PRIMARY)
keyboard_grade_choose.add_line()
keyboard_grade_choose.add_button('2')
keyboard_grade_choose.add_line()
keyboard_grade_choose.add_button('3', VkKeyboardColor.PRIMARY)
keyboard_grade_choose.add_line()
keyboard_grade_choose.add_button('4')
keyboard_grade_choose.add_line()
keyboard_grade_choose.add_button('Другое', VkKeyboardColor.PRIMARY)
keyboard_grade_choose.add_line()
keyboard_grade_choose.add_button('Все', VkKeyboardColor.POSITIVE)
keyboard_grade_choose.add_line()
keyboard_grade_choose.add_button('Назад', VkKeyboardColor.NEGATIVE)
#клавиатура команд для ручного управления группами бесед
keyboard_gb = VkKeyboard(one_time = False, inline = True)
keyboard_gb.add_button('Создать группу бесед', VkKeyboardColor.POSITIVE)
keyboard_gb.add_line()
keyboard_gb.add_button('Изменить название группы бесед', VkKeyboardColor.PRIMARY)
keyboard_gb.add_line()
keyboard_gb.add_button('Удалить группу бесед', VkKeyboardColor.NEGATIVE)
keyboard_gb.add_line()
keyboard_gb.add_button('Назад', VkKeyboardColor.NEGATIVE)
#клавиатура вывода групп
keyboard_group = VkKeyboard(one_time = False, inline = True)
keyboard_group.add_button('Все беседы', VkKeyboardColor.PRIMARY)
keyboard_group.add_line()
keyboard_group.add_button('Созданные группы', VkKeyboardColor.SECONDARY)
keyboard_group.add_line()
keyboard_group.add_button('Автоматически созданные группы', VkKeyboardColor.PRIMARY)
keyboard_group.add_line()
keyboard_group.add_button('Назад', VkKeyboardColor.NEGATIVE)
#Клавиатура "назад"
keyboard_back = VkKeyboard(one_time = False, inline = False)
keyboard_back.add_button('Назад', VkKeyboardColor.NEGATIVE)
session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(session, group_id)
def send_message_to_user (user_id, peer_id, message, keyboard=None): #сделать проще!
    post = {
        "user_id": user_id,
        "random_id": get_random_id(),
        "peer_id": peer_id,
        "message": message,
        "random_id": 0
    }
    if keyboard != None:
        post = {
        "user_id": user_id,
        "random_id": get_random_id(),
        "peer_id": peer_id,
        "message": message,
        "random_id": 0,
        "keyboard" : keyboard.get_keyboard()
        }
    session.method('messages.send', post)
def send_message_to_chat (chat_id, peer_id, message, keyboard=None): #сделать проще!
    post = {
        "chat_id": chat_id,
        "random_id": get_random_id(),
        "peer_id": peer_id,
        "message": message,
        "random_id": 0
    }
    if keyboard != None:
        post = {
        "chat": chat_id,
        "random_id": get_random_id(),
        "peer_id": peer_id,
        "message": message,
        "random_id": 0,
        "keyboard" : keyboard.get_keyboard()
        }
    session.method('messages.send', post)
def get_conversations(offset, count, filt):
    post = {
        "offset": offset,
        "count": count,
        "filter": filt
    }
    session.method("messages.getConversations", post)
def get_Conversations (peer_ids): 
    post = {
        "peer_ids": peer_ids
    }
    session.method("messages.getConversations", post)
conn = sqlite3.connect('chats_hse.db')
cursor = conn.cursor()
try:
    query = "CREATE TABLE \"chats\" (\"ID\" INTEGER UNIQUE, \"chat\" TEXT, \"program\" TEXT, \"grade\" TEXT, PRIMARY KEY (\"ID\"))"
    cursor.execute(query)
except:
    pass
#добавить группу в БД
def add_group_id(peer, text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO chats (ID, chat) VALUES (?, ?)',
                       (peer, text))
        con.commit()
def add_group_program(peer, text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('UPDATE chats SET program=(?) WHERE ID=(?)', (text.split()[1], peer_id))
        con.commit()
def add_group_grade(peer, text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('UPDATE chats SET grade=(?) WHERE ID=(?)', (text.split()[1], peer_id))
        con.commit()
def change_name(chat, peer_id):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('UPDATE chats SET chat=(?) WHERE ID=(?)', (chat, peer_id))
        con.commit()
#вывод списка групп по курсу
def choose_group_by_grade(text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM chats WHERE grade=(?)', (text,))
        groups, groups_dict = normal(cursor.fetchall())
    return groups, groups_dict
def choose_group_by_program(text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM chats WHERE program=(?)', (text,))
        groups, groups_dict = normal(cursor.fetchall())
    return groups, groups_dict
def choose_group_by_program_and_grade(grade, program):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM chats WHERE grade=(?) and program=(?)', (grade, program))
        groups, groups_dict = normal(cursor.fetchall())
    return groups, groups_dict
#вывод списка групп
def normal(st_group):
    groups = []
    groups_dict = defaultdict()
    for elem in st_group:
        chat_id = elem[0]
        group = elem[1]
        program = elem[2]
        grade = elem [3]
        groups.append((chat_id, group, program, grade))
        groups_dict[group]=(chat_id, program, grade)
    return groups, groups_dict
    
def choose_group():
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM chats')
        groups, groups_dict= normal(cursor.fetchall())
    return groups, groups_dict
#удаление беседы
def delete(text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('DELETE FROM chats WHERE chat=(?)', (text,))
        con.commit()
#вывод групп пользователю
def output(spisok, text):
    if len(spisok) <= 20:
        keyboard = VkKeyboard(one_time = False, inline = False)
        i = 0
        for elem in spisok:
            keyboard.add_button(elem)
            i+=1
            if i % 2 == 0:
                keyboard.add_line()
        keyboard.add_button('Назад')        
        send_message_to_user(user_id, peer_id, text, keyboard)
    else:
        spisok.append('Назад')
        send_message_to_user(user_id, peer_id, text + '\n'.join(spisok))
def sending(text):
    if text == 'да':
        if chosen_groups != []:
            send_message_to_user(user_id, peer_id, 'Рассылка началась')
            for elem in tqdm(chosen_groups):
                try:
                    print(elem[1])
                    send_message_to_chat(elem[1] - 2000000000, elem[1], msg)
                    time.sleep(0.1)

                except:
                    send_message_to_user(user_id, peer_id, 'В беседу: '+ f'{elem[0]}' + ' нет доступа')
            send_message_to_user(user_id, peer_id, 'Рассылка завершена')
            send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
            n = False
        else:
            send_message_to_user(user_id, peer_id, 'Выбранная группа не содержит ни одной беседы. Выберите другую группу или добавьте беседу',  keyboard_group) 
#             break
            n = False
    elif text in['отмена', 'Отмена']:
        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
        n = False
while True:
    
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.object['text'].lower()
                peer_id = event.obj.peer_id
        
                if event.from_user:#Если написали в ЛС
                    user_id = event.object['from_id']
                    
                    if text in ['начать', 'продолжить работу']:

                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)

#кнопка "отправить сообщение"
                    elif text == 'отправить сообщение':
                        send_message_to_user(user_id, peer_id, 'Выберите группу:', keyboard_group)
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                text = event.object['text']
                                peer_id = event.obj.peer_id
                                if text == 'Все беседы':
                                    chosen_groups = []
                                    groups, groups_dict = choose_group()
                                    send_message_to_user(user_id, peer_id, 'Выберите беседу:\n'+ '\n'.join([elem[1] for elem in groups]))
                                    send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_commands)

                                    n = True
                                    while n:
                                        for event in longpoll.listen():
                                            if event.type == VkBotEventType.MESSAGE_NEW:
                                                text = event.object['text']
                                                peer_id = event.obj.peer_id
                                                if text in list(groups_dict.keys()):
                                                    chosen_groups.append((groups_dict[text], text))
                                                    send_message_to_user(user_id, peer_id, 'Ещё одну?')
                                                    send_message_to_user(user_id, peer_id, 'Выберите беседу: \n' + '\n'.join([elem[1] for elem in groups]))
                                                    send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_commands)
                                                    n = True
                                                elif text == 'Выбрать все':
                                                    chosen_groups = groups
                                                    send_message_to_user(user_id, peer_id, 'Введите сообщение')
                                                    for event in longpoll.listen():
                                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                                            msg = event.object['text']
                                                            user_id = event.object['from_id']
                                                            send_message_to_user(user_id, peer_id, 'Вы отправляете сообщение: ' + f'{msg}' + ' следующим группам: '+ ', '.join([elem[1] for elem in chosen_groups]), keyboard_choice)

                                                            for event in longpoll.listen():
                                                                if event.type == VkBotEventType.MESSAGE_NEW:
                                                                    text = event.object['text'].lower()
                                                                    peer_id = event.obj.peer_id
                                                                    
                                                                    if text == 'да':
                                                                        if chosen_groups != []:
                                                                            send_message_to_user(user_id, peer_id, 'Рассылка началась')
                                                                            for elem in tqdm(chosen_groups):
                                                                                try:
                                                                                    print(elem[0])
                                                                                    send_message_to_chat(elem[0] - 2000000000, elem[0], msg)
                                                                                    time.sleep(0.1)

                                                                                except:
                                                                                    send_message_to_user(user_id, peer_id, 'В беседу: '+ f'{elem[1]}' + ' нет доступа')
                                                                            send_message_to_user(user_id, peer_id, 'Рассылка завершена')
                                                                            send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
                                                                            n = False
                                                                            break
                                                                        else:
                                                                            send_message_to_user(user_id, peer_id, 'Выбранная группа не содержит ни одной беседы. Выберите другую группу или добавьте беседу',  keyboard_group) 
                                                                #             break
                                                                            n = False
                                                                    elif text in['отмена', 'Отмена']:
                                                                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                                        n = False
                                                                        break
                                                            break
                                                    break

                                                elif text == 'Всё выбрано':
                                                    send_message_to_user(user_id, peer_id, 'Введите сообщение')
                                                    for event in longpoll.listen():
                                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                                            msg = event.object['text']
                                                            user_id = event.object['from_id']
                                                            send_message_to_user(user_id, peer_id, 'Вы отправляете сообщение: ' + f'{msg}'  + ' следующим группам: '+ ', '.join([elem[1] for elem in chosen_groups]), keyboard_choice)

                                                            for event in longpoll.listen():
                                                                if event.type == VkBotEventType.MESSAGE_NEW:
                                                                    text = event.object['text'].lower()
                                                                    peer_id = event.obj.peer_id
                                                                    if text == 'да':
                                                                        if chosen_groups != []:
                                                                            send_message_to_user(user_id, peer_id, 'Рассылка началась')
                                                                            for elem in tqdm(chosen_groups):
                                                                                try:
                                                                                    print(elem[0][0])
                                                                                    send_message_to_chat(elem[0][0] - 2000000000, elem[0][0], msg)
                                                                                    time.sleep(0.1)

                                                                                except:
                                                                                    send_message_to_user(user_id, peer_id, 'В беседу: '+ f'{elem[0]}' + ' нет доступа')
                                                                            send_message_to_user(user_id, peer_id, 'Рассылка завершена')
                                                                            send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
                                                                            n = False
                                                                            break
                                                                        else:
                                                                            send_message_to_user(user_id, peer_id, 'Выбранная группа не содержит ни одной беседы. Выберите другую группу или добавьте беседу',  keyboard_group) 
                                                                #             break
                                                                            n = False
                                                                    elif text in['отмена', 'Отмена']:
                                                                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                                        n = False
                                                                        break
                                                            break
                                                    break
                                                elif text == 'Назад':
                                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                    n = False
                                                    break
                                                elif text == 'Продолжить работу':
                                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                    n = False
                                                    break 
                                                    
                                                elif text == 'Пока всё':
                                                    send_message_to_user(user_id, peer_id, 'Если захотите продолжить работу, введите "начать"')
                                                    n = False
                                                    break 
                                                else:
                                                    send_message_to_user(user_id, peer_id, 'Такой группы нет. Выберите группу: \n'+'\n'.join([elem[1] for elem in groups]))
                                                    send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_commands)
                                    break 
                                elif text == 'Созданные группы': #улучшить - сделать выбор нескольких групп!!!!!!!!
                                    if list(handmade_list_of_groups.keys()) != []:
                                        b = list(handmade_list_of_groups.keys())
                                        output(b, 'Выберите группу: \n')
                                        for event in longpoll.listen():
                                            if event.type == VkBotEventType.MESSAGE_NEW:
                                                text = event.object['text']
                                                peer_id = event.obj.peer_id
                                                if text in b:
                                                    chosen_groups = handmade_list_of_groups[text]
                                                    send_message_to_user(user_id, peer_id, 'Введите сообщение')
                                                    for event in longpoll.listen():
                                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                                            msg = event.object['text']
                                                            user_id = event.object['from_id']
                                                            send_message_to_user(user_id, peer_id, 'Вы отправляете сообщение: ' + f'{msg}' + ' следующим группам: '+ ', '.join([elem[1] for elem in chosen_groups]), keyboard_choice)

                                                            for event in longpoll.listen():
                                                                if event.type == VkBotEventType.MESSAGE_NEW:
                                                                    text = event.object['text'].lower()
                                                                    peer_id = event.obj.peer_id
                                                                    sending(text)
                                                                    break
                                                            break
                                                else:
                                                    send_message_to_user(user_id, peer_id, 'Такой группы нет')
                                                    output(b, 'Выберите группу: \n')
                                                break
                                    
                                
                                    
                                    else:
                                        send_message_to_user(user_id, peer_id, 'Созданных групп нет')
                                        send_message_to_user(user_id, peer_id, 'Выберите группу:', keyboard_group) 
                    
                                elif text == 'Автоматически созданные группы':
                                    send_message_to_user(user_id, peer_id, 'Выберите курс', keyboard_grade_choose)
                                    for event in longpoll.listen():
                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                            grade = event.object['text']
                                            peer_id = event.obj.peer_id
                                            if grade in ['1', '2', '3', '4', 'Другое', 'Все']:
                                                send_message_to_user(user_id, peer_id, 'Выберите программу', keyboard_program_choose)
                                                for event in longpoll.listen():
                                                    if event.type == VkBotEventType.MESSAGE_NEW:
                                                        program = event.object['text']
                                                        peer_id = event.obj.peer_id
                                                        if program in ['Экономика', 'Экономика и статистика', 'Все', 'Другое']:
                                                            if grade != 'Все' and program != 'Все':
                                                                groups, groups_dict = choose_group_by_program_and_grade(grade, program)
                                                                chosen_groups = groups
                                                                send_message_to_user(user_id, peer_id, 'Введите сообщение')
                                                                for event in longpoll.listen():
                                                                    if event.type == VkBotEventType.MESSAGE_NEW:
                                                                        msg = event.object['text']
                                                                        user_id = event.object['from_id']
                                                                        send_message_to_user(user_id, peer_id, 'Вы отправляете сообщение: ' + f'{msg}' + ' следующим группам: '+ ', '.join([elem[1] for elem in groups]), keyboard_choice)

                                                                        for event in longpoll.listen():
                                                                            if event.type == VkBotEventType.MESSAGE_NEW:
                                                                                text = event.object['text'].lower()
                                                                                peer_id = event.obj.peer_id
                                                                                
                                                                                if text == 'да':
                                                                                    if chosen_groups != []:
                                                                                        send_message_to_user(user_id, peer_id, 'Рассылка началась')
                                                                                        for elem in tqdm(chosen_groups):
                                                                            #                 try:
                                                                                            print(elem[0])
                                                                                            send_message_to_chat(elem[0] - 2000000000, elem[0], msg)
                                                                                            time.sleep(0.1)

                                                                            #                 except:
                                                                            #                     send_message_to_user(user_id, peer_id, 'В беседу: '+ f'{elem[1]}' + ' нет доступа')
                                                                                        send_message_to_user(user_id, peer_id, 'Рассылка завершена')
                                                                                        send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
                                                                                        n = False
                                                                                        break
                                                                                    else:
                                                                                        send_message_to_user(user_id, peer_id, 'Выбранная группа не содержит ни одной беседы. Выберите другую группу или добавьте беседу',  keyboard_group) 
                                                                                        n = False
                                                                                elif text in['отмена', 'Отмена']:
                                                                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                                                    n = False
                                                                                    break
                                                                                break
                                                                        break
                                                                break
#                                                             break
                                                            elif grade != 'Все':
                                                                groups, groups_dict = choose_group_by_grade(grade)
                                                                chosen_groups = groups
                                                                send_message_to_user(user_id, peer_id, 'Введите сообщение')
                                                                for event in longpoll.listen():
                                                                    if event.type == VkBotEventType.MESSAGE_NEW:
                                                                        msg = event.object['text']
                                                                        user_id = event.object['from_id']
                                                                        send_message_to_user(user_id, peer_id, 'Вы отправляете сообщение: ' + f'{msg}' + ' следующим группам: '+ ', '.join([elem[1] for elem in groups]), keyboard_choice)

                                                                        for event in longpoll.listen():
                                                                            if event.type == VkBotEventType.MESSAGE_NEW:
                                                                                text = event.object['text'].lower()
                                                                                peer_id = event.obj.peer_id
                                                                                sending(text)
                                                                                break
                                                                        break
                                                            elif program != 'Все':
                                                                groups, groups_dict = choose_group_by_program(program)
                                                                chosen_groups = groups
                                                                send_message_to_user(user_id, peer_id, 'Введите сообщение')
                                                                for event in longpoll.listen():
                                                                    if event.type == VkBotEventType.MESSAGE_NEW:
                                                                        msg = event.object['text']
                                                                        user_id = event.object['from_id']
                                                                        send_message_to_user(user_id, peer_id, 'Вы отправляете сообщение: ' + f'{msg}' + ' следующим группам: '+ ', '.join([elem[1] for elem in groups]), keyboard_choice)

                                                                        for event in longpoll.listen():
                                                                            if event.type == VkBotEventType.MESSAGE_NEW:
                                                                                text = event.object['text'].lower()
                                                                                peer_id = event.obj.peer_id
                                                                                sending(text)
                                                                                break
                                                                        break
                                                         
                                                        elif program == 'Назад':
                                                            send_message_to_user(user_id, peer_id, 'Выберите курс', keyboard_grade_choose)
                                                        elif program == 'Пока всё':
                                                            send_message_to_user(user_id, peer_id, 'Если захотите продолжить работу, введите "начать"')
                                                            break
                                                        elif program == 'Продолжить работу':
                                                            send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                            break
                                                        else:
                                                            send_message_to_user(user_id, peer_id, 'Такой программы нет. Выберите программу', keyboard_program_choose) 
                                                        break
                                            elif grade == 'Назад':
                                                send_message_to_user(user_id, peer_id, 'Выберите группу:', keyboard_group)
                                            elif grade == 'Пока всё':
                                                send_message_to_user(user_id, peer_id, 'Если захотите продолжить работу, введите "начать"')
                                                break
                                            elif grade == 'Продолжить работу':
                                                send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                break
                                            else:
                                                send_message_to_user(user_id, peer_id, 'Такого курса нет. Выберите курс', keyboard_grade_choose)
                                
                                            break
#                                             break
#                                         break
                                elif text == 'Назад':
                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                    break
                            
                                elif text == 'Пока всё':
                                    send_message_to_user(user_id, peer_id, 'Если захотите продолжить работу, введите "начать"')
                                    break
                                
                                elif text == 'Продолжить работу':
                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                    break
                                    
                    
                    elif text == 'назад':
                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                        
                    
                    
# кнопка 'удалить беседу'
                    elif text == 'удалить беседу':
                        groups, groups_dict = choose_group()
#                         output(groups, 'Выберите группу, беседу которой хотите удалить: \n')
                        send_message_to_user(user_id, peer_id, 'Выберите группу, беседу которой хотите удалить: \n'+ '\n'.join([elem[1] for elem in groups]))
                        send_message_to_user(user_id, peer_id, 'Или нажмите кнопку ниже', keyboard_back)
        #получаем название удаляемой беседы
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                group = event.object['text']
                                peer_id = event.obj.peer_id
                                if group in list([elem[1] for elem in groups]):
                                    send_message_to_user(user_id, peer_id, 'Вы уверены? Действие нельзя будет отменить', keyboard_choice)
                                    #получаем подтверждение удаления
                                    for event in longpoll.listen():
                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                            text = event.object['text'].lower()
                                            peer_id = event.obj.peer_id
                                            if text == 'да':
                                                delete(group)
                                                send_message_to_user(user_id, peer_id, 'Беседа удалена')
                                                send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
                                                
                                            elif text == 'отмена':
                                                send_message_to_user(user_id, peer_id, 'Выберите группу, беседу которой хотите удалить: \n' + '\n'.join([elem[1] for elem in groups]))
                                                send_message_to_user(user_id, peer_id, 'Или нажмите кнопку ниже', keyboard_back)
                                            break
                                        
                                    
                                elif group == 'Назад':
                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                else:
                                    send_message_to_user(user_id, peer_id, 'Такой группы нет. Выберите группу: \n'+'\n'.join([elem[1] for elem in groups]))
                                    send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_0)
                     
                                break
#создание группы бесед вручную
                    elif text == 'управление группами бесед':
                        send_message_to_user(user_id, peer_id, 'Выберите действие', keyboard_gb)

                    elif text == 'создать группу бесед':
                        send_message_to_user(user_id, peer_id, 'Введите название группы')
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                group_name = event.object['text']
                                peer_id = event.obj.peer_id     
                                chosen_groups = []
                                groups, groups_dict = choose_group()
                                send_message_to_user(user_id, peer_id, 'Введите название беседы, которую хотите добавить в группу:\n'+ '\n'.join([elem[1] for elem in groups]), keyboard_choose_group_commands)

                                n = True
                                while n:
                                    for event in longpoll.listen():
                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                            text = event.object['text']
                                            peer_id = event.obj.peer_id
                                            if text in list(groups_dict.keys()):
                                                chosen_groups.append((groups_dict[text], text))
                                                send_message_to_user(user_id, peer_id, 'Ещё одну?')
                                                send_message_to_user(user_id, peer_id, 'Введите название беседы: \n' + '\n'.join([elem[1] for elem in groups]), keyboard_choose_group_commands)
                                                n = True
                                            elif text == 'Выбрать все':
                                                chosen_groups = groups
                                                handmade_list_of_groups[group_name]=chosen_groups
                                                send_message_to_user(user_id, peer_id, 'Создана группа бесед '+ f'{group_name}' + ' из бесед: ' +', '.join([elem[1] for elem in chosen_groups]))
                                                send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_gb)
                                                n = False
                                            elif text == 'Всё выбрано':
                                                if chosen_groups != []:
                                                    handmade_list_of_groups[group_name]=chosen_groups
                                                    send_message_to_user(user_id, peer_id, 'Создана группа бесед '+ f'{group_name}' + ' из бесед: ' +', '.join([elem[1] for elem in chosen_groups]))
                                                    send_message_to_user(user_id, peer_id,  'Что-то ещё?', keyboard_gb)
                                                    n = False
                                                else:
                                                    send_message_to_user(user_id, peer_id, 'Вы не выбрали ни одной беседы, группа не сформирована')
                                                    send_message_to_user(user_id, peer_id,  'Что-то ещё?', keyboard_gb)
                                                    n = False
                                            elif text == 'Назад':
                                                send_message_to_user(user_id, peer_id, 'Выберите действие', keyboard_gb)
                                                n = False
                                            break
                                break
        
        
                    elif text == 'изменить название группы бесед':
                        output(list(handmade_list_of_groups.keys()), "Введите название группы, которое хотите изменить:\n")
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                group_name = event.object['text']
                                peer_id = event.obj.peer_id
                                send_message_to_user(user_id, peer_id, 'Введите новое название группы')
                                if group_name in list(handmade_list_of_groups.keys()):
                                    for event in longpoll.listen():
                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                            new_group_name = event.object['text']
                                            peer_id = event.obj.peer_id
                                            a = handmade_list_of_groups[group_name]
                                            handmade_list_of_groups[new_group_name] = a
                                            del handmade_list_of_groups[group_name]
                                            send_message_to_user(user_id, peer_id, 'Название группы изменено')
                                            send_message_to_user(user_id, peer_id,  'Что-то ещё?', keyboard_gb)
                                            break
                                elif group_name == 'Назад':
                                    send_message_to_user(user_id, peer_id, 'Выберите действие', keyboard_gb)
                                break
                
                
                
                    elif text == 'удалить группу бесед':
                        output(list(handmade_list_of_groups.keys()), "Введите название группы, которую хотите удалить:\n")
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                group = event.object['text']
                                peer_id = event.obj.peer_id
                                if group in list(handmade_list_of_groups.keys()):
                                    send_message_to_user(user_id, peer_id, 'Вы уверены? Действие нельзя будет отменить', keyboard_choice)
                                    #получаем подтверждение удаления
                                    for event in longpoll.listen():
                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                            text = event.object['text'].lower()
                                            peer_id = event.obj.peer_id
                                            if text == 'да':
                                                del handmade_list_of_groups[group]
                                                send_message_to_user(user_id, peer_id, 'Группа удалена')
                                                send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_gb)

                                            elif text == 'отмена':
                                                output(list(handmade_list_of_groups.keys()), keyboard_group, "Введите название группы, которую хотите удалить:\n") 
                                            break
                                elif group == 'Назад':
                                    send_message_to_user(user_id, peer_id, 'Выберите действие', keyboard_start)

    #завершение работы
                    elif text == 'продолжить работу':
                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                    elif text == 'пока всё':
                        send_message_to_user(user_id, peer_id, 'Если захотите продолжить работу, введите "начать"')
                    elif text == 'Пока всё':
                        send_message_to_user(user_id, peer_id, 'Если захотите продолжить работу, введите "начать"')
                    else:
                        send_message_to_user(user_id, peer_id, 'Выберите один из вариантов ниже:', keyboard_start) 


                elif event.from_chat:
                    chat_id = event.chat_id
                    if text == 'регистрация':
                        send_message_to_chat(chat_id, peer_id, 'Введите название своей группы')
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                text = event.object['text']
                                peer_id = event.obj.peer_id
                                try:
                                    add_group_id(peer_id, text)
                                    send_message_to_chat(chat_id, peer_id, 'Принято. Выберите вашу программу', keyboard_program)
                                    for event in longpoll.listen():
                                        if event.type == VkBotEventType.MESSAGE_NEW:
                                            text = event.object['text']
                                            peer_id = event.obj.peer_id
                                            add_group_program(peer_id, text)
                                            send_message_to_chat(chat_id, peer_id, 'Принято. Выберите ваш курс обучения', keyboard_grade)
                                            for event in longpoll.listen():
                                                if event.type == VkBotEventType.MESSAGE_NEW:
                                                    text = event.object['text']
                                                    peer_id = event.obj.peer_id
                                                    add_group_grade(peer_id, text)
                                                    send_message_to_chat(chat_id, peer_id, 'Принято')
                                                    break
                                            break
                                except:
                                    send_message_to_chat(chat_id, peer_id, 'Беседа уже зарегистрирована')
                                break
                                
                    elif text == 'изменить название группы':
                        send_message_to_chat(chat_id, peer_id, 'Введите новое название своей группы')
                        
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                chat_id = event.chat_id
                                peer_id = event.obj.peer_id
                                text = event.object['text']
                                change_name(text, peer_id)
                                send_message_to_chat(chat_id, peer_id, 'Название изменено')
                                break
                    elif text == 'изменить программу':
                        send_message_to_chat(chat_id, peer_id, 'Выберите вашу программу', keyboard_program)
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                text = event.object['text']
                                peer_id = event.obj.peer_id
                                add_group_program(peer_id, text)
                                send_message_to_chat(chat_id, peer_id, 'Программа изменена')
                                break
                    elif text == 'изменить курс':
                        send_message_to_chat(chat_id, peer_id, 'Выберите ваш курс обучения', keyboard_grade)
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                text = event.object['text']
                                peer_id = event.obj.peer_id
                                add_group_grade(peer_id, text)
                                send_message_to_chat(chat_id, peer_id, 'Курс изменён')
                                break
                        
#             if event.type == VkBotEventType.MESSAGE_EVENT: #callback-кнопки   
#                 print(event)

                
    except requests.exceptions.ReadTimeout as timeout:
        continue
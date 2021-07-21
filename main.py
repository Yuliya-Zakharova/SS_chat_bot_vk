import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import sqlite3
from collections import defaultdict
from vk_api.utils import get_random_id
import time
token = '9bcd41d111a6408d9674faf43b068059ff5d1eef84153ca40d9488ed47b2ee4799bddbac0024e96b5c723'
group_id = '205976516'
version = '5.103'
group_name_short = 'sendler_ss'
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
def vk_download(method, parameters, fields=''):
    url = 'https://api.vk.com/method/' + method + '?' + parameters + '&fields=' + fields + '&access_token=' + token + '&v=' + version
    response = requests.get(url)
    infa = response.json()
    return infa
conn = sqlite3.connect('chats_hse.db')
cursor = conn.cursor()

try:
    query = "CREATE TABLE \"chats\" (\"ID\" INTEGER UNIQUE, \"chat\" TEXT, PRIMARY KEY (\"ID\"))"
    cursor.execute(query)
except:
    pass
#добавить группу в БД
def add_group(peer, text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO chats (ID, chat) VALUES (?, ?)',
                       (peer, text))
        con.commit()
#вывод списка групп
#вывод списка групп
def normal(st_group):
    groups = []
    groups_dict = defaultdict()
    for elem in st_group:
        chat_id = elem[0]
        group = elem[1]
        groups.append((chat_id, group))
        groups_dict[group]=chat_id
    return groups, groups_dict
    
def choose_group():
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM chats')
        groups, groups_dict= normal(cursor.fetchall())
    return groups, groups_dict
#изменение название группы
def change_name(chat, peer_id):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('UPDATE chats SET chat=(?) WHERE ID=(?)', (chat, peer_id))
        con.commit()
#удаление беседы
def delete(text):
    with sqlite3.connect('chats_hse.db') as con:
        cursor = con.cursor()
        cursor.execute('DELETE FROM chats WHERE chat=(?)', (text,))
        con.commit()
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
keyboard_start.add_button('Удалить беседу', VkKeyboardColor.NEGATIVE)
keyboard_start.add_line()
keyboard_start.add_button('Отправить сообщение', VkKeyboardColor.SECONDARY)
keyboard_start.add_line()
keyboard_start.add_button('Пока всё', VkKeyboardColor.POSITIVE)
#клавиатура команд для отправки сообщений
keyboard_choose_group_commands = VkKeyboard(one_time = False, inline = True)
keyboard_choose_group_commands.add_button('Всё выбрано. Ввести сообщение', VkKeyboardColor.SECONDARY)
keyboard_choose_group_commands.add_line()
keyboard_choose_group_commands.add_button('Выбрать все', VkKeyboardColor.PRIMARY)
keyboard_choose_group_commands.add_line()
keyboard_choose_group_commands.add_button('Назад', VkKeyboardColor.NEGATIVE)
#клавиатура команд для удаления бесед
keyboard_choose_group_delete = VkKeyboard(one_time = False, inline = True)
keyboard_choose_group_delete.add_button('Выбрать все', VkKeyboardColor.PRIMARY)
keyboard_choose_group_delete.add_line()
keyboard_choose_group_delete.add_button('Назад', VkKeyboardColor.NEGATIVE)
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
                        chosen_groups = []
                        groups, groups_dict = choose_group()
                        send_message_to_user(user_id, peer_id, 'Выберите группу:\n'+ '\n'.join([elem[1] for elem in groups]))
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
                                        send_message_to_user(user_id, peer_id, 'Выберите группу: \n' + '\n'.join([elem[1] for elem in groups]))
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
                                                                        send_message_to_chat(elem[0] - 2000000000, elem[0], msg)
                                                                        time.sleep(0.1)

                                                                    except:
                                                                        send_message_to_user(user_id, peer_id, 'В беседу: '+ f'{elem[1]}' + ' нет доступа')
                                                                send_message_to_user(user_id, peer_id, 'Рассылка завершена')
                                                                send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
                                                                n = False

                                                                break
                                                            else:
                                                                send_message_to_user(user_id, peer_id, 'Вы не выбрали ни одной группы. Выберите группу', keyboard_choose_group_commands) 
                                                                n = False
                                                        elif text == 'отмена':
                                                            send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                            n = False
                                                            break
                                                break
                                        
                                    
                                    elif text == 'Всё выбрано. Ввести сообщение':
                                        if chosen_groups != []: 
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
                                                                send_message_to_user(user_id, peer_id, 'Рассылка началась')
                                                                for elem in tqdm(chosen_groups):
                                                                    try:
                                                                        send_message_to_chat(elem[0] - 2000000000, elem[0], msg)
                                                                        time.sleep(0.1)
                                                                    except:
                                                                        send_message_to_user(user_id, peer_id, 'В беседу: '+ f'{elem[1]}' + ' нет доступа')
                                                                send_message_to_user(user_id, peer_id, 'Рассылка завершена')
                                                                send_message_to_user(user_id, peer_id, 'Что-то ещё?', keyboard_end)
                                                                n = False
                                                            elif text == 'отмена':
                                                                send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                                                n = False
                                                                break
                                                    break
                                        else:
                                            send_message_to_user(user_id, peer_id, 'Вы не выбрали ни одной группы. Выберите группу: \n'+'\n'.join([elem[1] for elem in groups]), keyboard_choose_group_commands) 
                                            n = False
                                                      

                                    elif text == 'Назад':
                                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                        n = False
                                    else:
                                        send_message_to_user(user_id, peer_id, 'Такой группы нет. Выберите группу: \n'+'\n'.join([elem[1] for elem in groups]))
                                        send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_commands)
                                    break
                                       
                    elif text == 'назад':
                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                        
                    
                    
# кнопка 'удалить беседу'
                    elif text == 'удалить беседу':
                        groups, groups_dict = choose_group()
                
                        send_message_to_user(user_id, peer_id, 'Выберите группу, беседу которой хотите удалить: \n'+ '\n'.join([elem[1] for elem in groups]))
                        send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_delete)

        #получаем название удаляемой группы
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
                                                send_message_to_user(user_id, peer_id, 'Выберите группу, беседу которой хотите удалить' + '\n'.join([elem[1] for elem in groups])) 
                                            break
                                        
                                    
                                elif group == 'Назад':
                                    send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                                else:
                                    send_message_to_user(user_id, peer_id, 'Такой группы нет. Выберите группу: \n'+'\n'.join([elem[1] for elem in groups]))
                                    send_message_to_user(user_id, peer_id, 'Команды', keyboard_choose_group_delete)
                     
                                break
                    
#завершение работы
                    elif text == 'продолжить работу':
                        send_message_to_user(user_id, peer_id, 'Что сделать?', keyboard_start)
                    elif text == 'пока всё':
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
                                    add_group(peer_id, text)
                                    send_message_to_chat(chat_id, peer_id, 'Принято')
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

                        
#             if event.type == VkBotEventType.MESSAGE_EVENT: #callback-кнопки   
#                 print(event)

                
    except requests.exceptions.ReadTimeout as timeout:
        continue
# -*- coding: utf-8 -*-
import json
import requests
from settings import API_URL, TOKEN, ADMIN_TOKEN


class WABot():
    def __init__(self, json, forward_table):
        self.json = json
        self.dict_messages = json.get('messages', [])
        self.APIUrl = API_URL
        self.token = TOKEN
        self.forward_table = forward_table
        self.chats_list = self.get_chat_list()

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_get_request(self, method):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.get(url, headers=headers)
        return answer.json()

    def send_message(self, phone, text):
        data = {"phone": phone,
                "body": text}
        answer = self.send_requests('sendMessage', data)
        return answer

    def forward_message(self, destination, message):
        data = {"messageId": message['id']}
        data.update(destination)  # Add chatId or phone
        answer = self.send_requests('forwardMessage', data)
        return answer

    def get_chat_id(self, chat_name):
        for chat in self.chats_list:
            if chat['name'] == chat_name:
                return chat['id']
            continue
        return False

    def get_chat_list(self):
        all_chats = self.send_get_request('dialogs')
        return all_chats['dialogs']

    def get_source(self, message, author):
        if '-' in message['chatId']:
            source = message['chatName']
        else:
            source = author.replace('@c.us', '')
        return source

    def get_destination(self, redirect_info):
        if redirect_info.isdigit():
            destination = {'phone': redirect_info}
        else:
            chat_id = self.get_chat_id(redirect_info)
            destination = {'chatId': chat_id}
        return destination

    def handle_command(self, command, phone):
        command = command.split()
        if command[1] != ADMIN_TOKEN:
            self.send_message(phone, 'НЕПРАВИЛЬНЫЙ ТОКЕН')
            return False
        command_type = command[2].lower()
        if command_type == 'add':
            self.forward_table.add_route(command[3], command[4])
            forward_table = self.forward_table.like_str()
            message = f"Маршрут добавлен.\nТаблица маршрутизации:\n{forward_table}"
        elif command_type == 'delete':
            self.forward_table.remove_route(command[3])
            forward_table = self.forward_table.like_str()
            message = f"Маршрут удален.\nТаблица маршрутизации:\n{forward_table}"
        elif command_type == 'show':
            forward_table = self.forward_table.like_str()
            message = f"Таблица маршрутизации:\n{forward_table}"
        elif command_type == 'clean':
            forward_table = self.forward_table.like_str()
            self.forward_table.clean_table()
            message = "Таблица маршрутизации очищена"
        self.send_message(phone, message)
        return "OK"

    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                author = message['author']
                if 'command' in message['body'].lower():
                    self.handle_command(message['body'], author.replace('@c.us', ''))
                    return "OK"
                if message['fromMe']:
                    return "Message from bot"
                source = self.get_source(message, author)
                redirect_info = self.forward_table.table.get(source, False)
                if not redirect_info:
                    return "No source in redirect table"
                destination = self.get_destination(redirect_info)
                self.forward_message(destination, message)
                return "OK"
        return "No messeges"

import json
import requests
from settings import API_URL, TOKEN, redirect


class WABot():    
    def __init__(self, json):
        self.json = json
        self.dict_messages = json.get('messages', [])
        self.APIUrl = API_URL
        self.token = TOKEN

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, phone, text):
        data = {"phone": phone,
                "body": text}
        answer = self.send_requests('sendMessage', data)
        return answer

    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                print(message)
                if message['fromMe']:
                    return "This message from me"
                phone = message['author'].replace('@c.us', '')
                text = 'From bot:' + message['body']
                print(message)
                redirect_phone = redirect.get(phone, False)
                if redirect_phone:
                    self.send_message(redirect_phone, text)
                    return 'OK'
                return "Havent number for redirect"
        return "No message for redirect"

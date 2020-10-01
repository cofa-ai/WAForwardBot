import requests
import json

from settings import TOKEN, API_URL


"""
{
  "webhookUrl": "http://bin.chat-api.com/1f9aj261",
  "ackNotificationsOn": true,
  "chatUpdateOn": null,
  "videoUploadOn": null,
  "proxy": "null,
  "guaranteedHooks": null,
  "ignoreOldMessages": null,
  "processArchive": null,
  "instanceStatuses": null,
  "webhookStatuses": null,
  "statusNotificationsOn": null
}
"""


def send_requests(method, data):
    url = f"{API_URL}{method}?token={TOKEN}"
    headers = {'Content-type': 'application/json'}
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    return answer.json()


def send_get_request(method):
    url = f"{API_URL}{method}?token={TOKEN}"
    headers = {'Content-type': 'application/json'}
    answer = requests.get(url, headers=headers)
    return answer.json()


def change_webhook_url(hook_server):
    data = {"webhookUrl": f"http://{hook_server}"}
    send_requests('settings', data)


def get_settings():
    return send_get_request('settings')


if __name__ == '__main__':
    server = "192.168.10.21:5000"
    change_webhook_url(server)

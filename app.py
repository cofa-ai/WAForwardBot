from flask import Flask, request
from WABot.wabot import WABot
from WABot.forward_table import ForwaradTable
from settings import forward_table_path


app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        forward_table = ForwaradTable(forward_table_path)
        bot = WABot(request.json, forward_table)
        handle = bot.processing()
        return handle


if(__name__) == '__main__':
    app.run("0.0.0.0", 5000)

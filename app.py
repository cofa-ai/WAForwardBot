from flask import Flask, request
from wabot import WABot


app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        handle = bot.processing()
        return handle


if(__name__) == '__main__':
    app.run()
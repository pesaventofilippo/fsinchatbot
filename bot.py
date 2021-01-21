# Python Libraries
from time import sleep
from telepotpro import Bot, glance
from telepotpro.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from threading import Thread
from json import load as jsload
from os.path import abspath, dirname, join
from modules import keyboards

with open(join(dirname(abspath(__file__)), "settings.json")) as settings_file:
    js_settings = jsload(settings_file)

bot = Bot(js_settings["token"])
dataMap = {}


def reply(msg):
    chatId = msg['chat']['id']

    if chatId > 0:
        bot.sendMessage(chatId, "Hi! I'm the Fs In Chat Bot 👋\n"
                                "You can type @fsinchatbot on any chat to display a message "
                                "with a button every user can press to pay respects!\n\n"
                                "Press the button below to try now!", parse_mode="HTML", reply_markup=keyboards.tryInline())


def button_press(msg):
    msgIdent = msg['inline_message_id']
    button, data = msg['data'].split("#", 1)

    if button == "pressf":
        count = int(data)
        if msgIdent not in dataMap:
            dataMap[msgIdent] = count
        dataMap[msgIdent] += 1
        try:
            bot.editMessageReplyMarkup(msgIdent, keyboards.pressF(dataMap[msgIdent]))
        except Exception:
            pass


def query(msg):
    queryId, chatId, queryString = glance(msg, flavor="inline_query")
    desc = f" for {queryString}" if queryString else " to pay respect."

    results = [
        InlineQueryResultArticle(
            id=f"pressf_{queryString}",
            title="Press F",
            input_message_content=InputTextMessageContent(
                message_text=f"<b>Press F</b>{desc}",
                parse_mode="HTML"
            ),
            reply_markup=keyboards.pressF(),
            description=desc,
            thumb_url="https://i.imgur.com/Nc7b9Yx.png"
        )
    ]
    bot.answerInlineQuery(queryId, results, cache_time=10800, is_personal=False)


def accept_message(msg):
    Thread(target=reply, args=[msg]).start()

def accept_button(msg):
    Thread(target=button_press, args=[msg]).start()

def incoming_query(msg):
    Thread(target=query, args=[msg]).start()

bot.message_loop(
    callback={'chat': accept_message, 'callback_query': accept_button, 'inline_query': incoming_query}
)

while True:
    sleep(60)

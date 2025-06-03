from pony.orm import db_session
from json import load as jsload
from flask import Flask, request
from telepotpro import Bot, glance
from telepotpro.loop import OrderedWebhook
from os.path import abspath, dirname, join
from telepotpro.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from modules import keyboards
from modules.database import Counter

with open(join(dirname(abspath(__file__)), "settings.json")) as settings_file:
    js_settings = jsload(settings_file)

app = Flask(__name__)
bot = Bot(js_settings["token"])


def reply(msg):
    chatId = msg['chat']['id']
    if chatId > 0:
        bot.sendMessage(chatId, "Hi! I'm the Fs In Chat Bot 👋\n"
                                "You can type @fsinchatbot on any chat to display a message "
                                "with a button every user can press to pay respects!\n\n"
                                "Press the button below to try now!", reply_markup=keyboards.tryInline())


@db_session
def button(msg):
    queryId = msg['id']
    msgId = str(msg['inline_message_id'])
    text = str(msg['data'])

    if not Counter.get(msgId=msgId):
        Counter(msgId=msgId)
    counter = Counter.get_for_update(msgId=msgId)
    if "#" in text:
        prev_count = int(text.split("#")[1])
        counter.count = prev_count
    counter.count += 1

    if text == "pressf":
        bot.answerCallbackQuery(queryId, "F added.")
        bot.editMessageReplyMarkup(msgId, keyboards.pressF(counter.count))
    elif text == "oneclick":
        bot.answerCallbackQuery(queryId, "Click added.")
        bot.editMessageReplyMarkup(msgId, keyboards.oneClick(counter.count))


def query(msg):
    queryId, chatId, queryString = glance(msg, flavor="inline_query")

    pressF_desc = queryString if queryString else "to pay respect."
    oneClick_desc = queryString if queryString else "1 like"

    results = [
        InlineQueryResultArticle(
            id=f"pressf_{queryString}",
            title="Press F",
            input_message_content=InputTextMessageContent(
                message_text=f"<b>Press F</b> {pressF_desc}",
                parse_mode="HTML"
            ),
            reply_markup=keyboards.pressF(),
            description=pressF_desc,
            thumb_url="https://i.imgur.com/Nc7b9Yx.png"
        ),
        InlineQueryResultArticle(
            id=f"oneclick_{queryString}",
            title="1 click =",
            input_message_content=InputTextMessageContent(
                message_text=f"<b>1 Click =</b> {oneClick_desc}",
                parse_mode="HTML"
            ),
            reply_markup=keyboards.oneClick(),
            description=oneClick_desc,
            thumb_url="https://i.imgur.com/Nc7b9Yx.png"
        )
    ]
    bot.answerInlineQuery(queryId, results, cache_time=3600, is_personal=False)


webhook = OrderedWebhook(bot, {'chat': reply, 'callback_query': button, 'inline_query': query})
@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'ok', 200


if __name__ == "__main__":
    bot.setWebhook(js_settings["webhook_url"])
    webhook.run_as_thread()
    app.run("127.0.0.1", port=js_settings["web_port"], debug=False)

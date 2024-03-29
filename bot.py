from telepotpro import Bot, glance, api as tgapi
from telepotpro.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from time import sleep
from json import load as jsload
from os.path import abspath, dirname, join
from pony.orm import db_session
from modules import keyboards
from modules.database import Counter

with open(join(dirname(abspath(__file__)), "settings.json")) as settings_file:
    js_settings = jsload(settings_file)
    if js_settings.get("api_server"):
        tgapi.set_api_url(js_settings["api_server"])

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


bot.message_loop({'chat': reply, 'callback_query': button, 'inline_query': query})
while True:
    sleep(60)

from telepotpro import Bot, glance
from telepotpro.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from time import sleep
from json import load as jsload
from os.path import abspath, dirname, join
from modules import keyboards


with open(join(dirname(abspath(__file__)), "settings.json")) as settings_file:
    js_settings = jsload(settings_file)

bot = Bot(js_settings["token"])


def reply(msg):
    chatId = msg['chat']['id']
    if chatId > 0:
        bot.sendMessage(chatId, "Hi! I'm the Fs In Chat Bot 👋\n"
                                "You can type @fsinchatbot on any chat to display a message "
                                "with a button every user can press to pay respects!\n\n"
                                "Press the button below to try now!", reply_markup=keyboards.tryInline())


def button_press(msg):
    msgIdent = msg['inline_message_id']
    button, data = msg['data'].split("#", 1)

    if button == "pressf":
        bot.editMessageReplyMarkup(msgIdent, keyboards.pressF(int(data)+1))
    elif button == "oneclick":
        bot.editMessageReplyMarkup(msgIdent, keyboards.oneClick(int(data)+1))


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
    bot.answerInlineQuery(queryId, results, cache_time=10800, is_personal=False)


bot.message_loop(callback={'chat': reply, 'callback_query': button_press, 'inline_query': query})

while True:
    sleep(60)

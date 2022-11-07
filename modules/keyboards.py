from telepotpro.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def tryInline():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="💬 Press F in a chat", switch_inline_query="")
    ]])


def pressF(count: int=0):
    txt = "Press F" if count == 0 else "1 F in Chat" if count == 1 else f"{count} F's"
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=txt, callback_data="pressf")
    ]])


def oneClick(desc: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=desc, callback_data="oneclick")
    ]])

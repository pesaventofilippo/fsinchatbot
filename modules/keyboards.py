from telepotpro.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def tryInline():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="💬 Press F in a chat", switch_inline_query="")
    ]])


def pressF(count: int=0):
    if count == 0:
        txt = "Press F"
    elif count == 1:
        txt = "1 F in Chat"
    else:
        txt = f"{count} F's"
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=txt, callback_data=f"pressf#{count}")
    ]])

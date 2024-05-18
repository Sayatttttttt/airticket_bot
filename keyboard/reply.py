from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def location_keyboard(locations: list[str]):
    locations.append("Отмена")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=i)] for i in locations
        ],
        resize_keyboard=True
    )
    return keyboard

def confirm_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Все правильно")],
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )
    return keyboard

def tariffs_keyboard(tariffs: list[str]):
    tariffs.append("Отмена")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=i)] for i in tariffs
        ],
        resize_keyboard=True
    )
    return keyboard

def menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Купить билет")],
            [KeyboardButton(text="Мои билеты")],
            [KeyboardButton(text="Отменить билет")],
            [KeyboardButton(text="Оплатить")]
        ],
        resize_keyboard=True
    )
    return keyboard
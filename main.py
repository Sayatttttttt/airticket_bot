import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, TECH_SUPPORT
from database import db
from keyboard import reply as kb

from handlers.payments import payments_router
from handlers.flights import flights_router
from handlers.order import order_router


dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    await message.reply(f"Приветствую вас!\nВы можете у нас купить билеты на самолет\nДля помощи введите команду /help", reply_markup=kb.menu_keyboard())

@dp.message(Command(commands="help"))
async def echo_handler(message: Message):
    await message.answer(
            (
            "Команды бота:\n"
            "/start - Начать диалог с ботом\n"
            "/flights или /tickets - Посмотреть ваши билеты\n"
            "/order или /new -  купить новый билет\n"
            "/pay или /buy - оплатить билет, проверить задолженность\n\n"
            "Техническая поддержка:\n"
            f'{html.link("Служба поддержки (тык)", TECH_SUPPORT)}'
            ), reply_markup=kb.menu_keyboard()
        )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(payments_router)
    dp.include_router(order_router)
    dp.include_router(flights_router)

    db.create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
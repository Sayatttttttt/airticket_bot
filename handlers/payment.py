from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery, ContentType

from config import PRICE, PAYMENT_TOKEN

payment_router = Router()

@payment_router.message(Command(commands=["pay", "buy"]))
async def sub_bay(message: Message, bot: Bot):
    await bot.send_invoice(message.from_user.id,
                           title="За деньги да!",
                           description="Инстасамец, не знаю что еще",
                           provider_token=PAYMENT_TOKEN,
                           currency="uzs",
                           photo_url="https://cdn.ananasposter.ru/image/cache/catalog/poster/pos23/13/64114-250x250.jpg",
                           photo_width=250,
                           photo_height=250,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="for-money-yes",
                           payload="test-invoice-payload-idk")
    

@payment_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@payment_router.message(F.content_types == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await message.answer('Оплата прошла успешно!')
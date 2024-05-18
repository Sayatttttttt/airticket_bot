from aiogram import F, Bot, Router, html
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery, ContentType

from config import ECONOMY_PRICE, BUSINESS_PRICE, PAYMENT_TOKEN, TECH_SUPPORT
from database import db
from keyboard import reply as kb


payments_router = Router()

@payments_router.message(Command(commands=["pay", "buy"]))
@payments_router.message(F.text == "Оплатить")
async def sub_bay(message: Message, bot: Bot):
    unpaid = db.get_flight_by_user_id_status(message.from_user.id, 0)
    if unpaid:
        price = ECONOMY_PRICE if unpaid[0].tariff == "Эконом" else BUSINESS_PRICE
        await bot.send_invoice(message.from_user.id,
                            title="Оплата",
                            description="Оплата за билет в самолет",
                            provider_token=PAYMENT_TOKEN,
                            currency="uzs",
                            photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsBTT35Uu2tAGrvRDgYgkCJNJQpnT5Ae_RiZCRmPAjqg&s",
                            photo_width=830,
                            photo_height=552,
                            photo_size=416,
                            is_flexible=False,
                            prices=[price],
                            start_parameter="ticket-payment",
                            payload="test-invoice-payload-idk")
    else:
        await message.answer("У вас всё оплачено!", reply_markup=kb.menu_keyboard())
    

@payments_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@payments_router.message(F.content_types == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    unpaid_flights = db.get_flight_by_user_id_status(message.from_user.id, 0)
    updated = db.update_flight_status(unpaid_flights[0].fid, 1)

    if updated:
        await message.answer('Оплата прошла успешно!', reply_markup=kb.menu_keyboard())
    else:
        await message.answer(f'Что-то пошло не так, свяжитесь со службой поддержки!\n{html.link("Служба поддержки (тык)", TECH_SUPPORT)}', reply_markup=kb.menu_keyboard())
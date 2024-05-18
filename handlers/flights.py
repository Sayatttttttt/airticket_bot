from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from database import db
from keyboard import reply as kb


flights_router = Router()

@flights_router.message(Command(commands={"flights", "tickets"}))
@flights_router.message(F.text == "Мои билеты")
async def flights_handler(message: Message):
    db_tickets = db.get_flights_by_user_id(message.from_user.id)
    
    if not db_tickets:
        await message.answer("У вас нету билетов!", reply_markup=kb.menu_keyboard())
        return

    tickets = [str(i)+"\n\n" for i in db_tickets]
    text = "Ваши билеты:\n\n"+"\n\n".join(tickets)

    await message.answer(text, reply_markup=kb.menu_keyboard())

@flights_router.message(Command(commands={"cancel_flight"}))
@flights_router.message(F.text == "Отменить билет")
async def flights_handler(message: Message):
    unpaid = db.get_flight_by_user_id_status(message.from_user.id, 0)

    if not unpaid:
        await message.answer("У вас нету долгов!", reply_markup=kb.menu_keyboard())
        return

    for i in unpaid:
        db.delete_flight_by_fid(i.fid)
    
    await message.answer("Покупка билета отменена", reply_markup=kb.menu_keyboard())
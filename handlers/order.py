from aiogram import F, Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database import db
from handlers.payments import sub_bay
from states import OrderFlight
from config import locations, tariffs, prices, TECH_SUPPORT
from keyboard import reply as kb


order_router = Router()

@order_router.message(Command(commands=["cancel"]))
@order_router.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext):
    await message.answer("Отменено", reply_markup=kb.menu_keyboard())
    await state.clear()

@order_router.message(StateFilter(None), Command(commands=["order", "new"]))
@order_router.message(StateFilter(None), F.text == "Купить билет")
async def location_handler(message: Message, bot: Bot, state: FSMContext):
    unpaid_tickets = db.get_flight_by_user_id_status(message.from_user.id, 0)

    if unpaid_tickets:
        await message.answer("Прежде чем купить новый билет, оплатите неоплаченный, или же отмените его командой /cancel_flight", reply_markup=kb.menu_keyboard())
        await sub_bay(message, bot)
        return
    
    locs = locations[:]
    await message.answer("Выберите место отлета", reply_markup=kb.location_keyboard(locs))
    await state.set_state(OrderFlight.location)

@order_router.message(OrderFlight.location, F.text.in_(locations))
async def destination_handler(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    destinations = [i for i in locations if i != message.text]
    await message.answer("Выберите место прибытия", reply_markup=kb.location_keyboard(destinations))
    await state.set_state(OrderFlight.destination)

@order_router.message(OrderFlight.location)
async def location_error_handler(message: Message, state: FSMContext):
    locs = locations[:]
    await message.answer(f"Выберите правильное место отлета из списка ниже или нажмите на кнопку:\n{', '.join(locations)}", reply_markup=kb.location_keyboard(locs))

@order_router.message(OrderFlight.destination, F.text.in_(locations))
async def tariff_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text == data['location']:
        destinations = [i for i in locations if i != data['location']]
        await message.answer(f"Выберите правильное место отлета из списка ниже или нажмите на кнопку:\n{', '.join(destinations)}", reply_markup=kb.location_keyboard(destinations))
        return
    
    await state.update_data(destination=message.text)
    await message.answer("Выберите тариф", reply_markup=kb.tariffs_keyboard(tariffs))
    await state.set_state(OrderFlight.tariff)

@order_router.message(OrderFlight.destination)
async def destination_error_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    destinations = [i for i in locations if i != data['location']]
    await message.answer(f"Выберите правильное место отлета из списка ниже или нажмите на кнопку:\n{', '.join(destinations)}", reply_markup=kb.location_keyboard(destinations))

@order_router.message(OrderFlight.tariff, F.text.in_(tariffs))
async def confirm_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    departure = datetime.now() + timedelta(days=3)
    arrival = departure + timedelta(hours=3)
    price = prices[message.text]
    flight = "AA123456"

    await state.update_data(tariff=message.text, departure=departure, arrival=arrival, flight=flight, price=price)
    
    await message.answer(
        (
            "Подтвердите правильность данных:\n\n"
            f"Откуда: {data['location']}\n"
            f"Куда: {data['destination']}\n"
            f"Время вылета: {departure}\n"
            f"Время прибытия: {arrival}\n"
            f"Тариф: {message.text}\n"
            f"Рейс: {flight}\n"
            f"Цена: {price}\n\n"
            "Для отмены введите любое сообщение кроме сообщения подтверждения или же воспользуйтесь командой /cancel"
        ), reply_markup=kb.confirm_keyboard()
    )
    await state.set_state(OrderFlight.confirm)

@order_router.message(OrderFlight.tariff)
async def tariff_error_handler(message: Message, state: FSMContext):
    await message.answer(f"Выберите правильный тариф из списка ниже или нажмите на кнопку:\n{', '.join(tariffs)}", reply_markup=kb.tariffs_keyboard(tariffs))

@order_router.message(OrderFlight.confirm, F.text.in_(["Все правильно"]))
async def create_order_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    created = db.insert_flight(
        status=0, user_id=message.from_user.id, location=data['location'],
        destination=data['destination'], departure=data['departure'], arrival=data['arrival'],
        flight=data['flight'], price=data['price'], tariff=data['tariff']
    )
    if created:
        await message.answer("Успешно создано! Теперь, оплатите билет", reply_markup=kb.menu_keyboard())
        await sub_bay(message, bot)
    else:
        await message.answer(f'Что-то пошло не так, свяжитесь со службой поддержки!\n{html.link("Служба поддержки (тык)", TECH_SUPPORT)}', reply_markup=kb.menu_keyboard())
    
    await state.clear()

@order_router.message(OrderFlight.confirm)
async def create_order_error_handler(message: Message, state: FSMContext):
    await message.answer(f"Покупка билета отменена!")
    await state.clear()

from aiogram.fsm.state import State, StatesGroup

class OrderFlight(StatesGroup):
    location = State()
    destination = State()
    tariff = State()
    confirm = State()
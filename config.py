from aiogram.types import LabeledPrice

TOKEN = "6877052402:AAGXgWf5LwLlwg4qsvwU9bF-2kFPifwR1rA"

PAYMENT_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"
ECONOMY_PRICE = LabeledPrice(label="Оплата за билет", amount=499_900*100) # считает в копейках, поэтому умножаем на 100
BUSINESS_PRICE = LabeledPrice(label="Оплата за билет", amount=999_900*100)

TECH_SUPPORT = "https://t.me/Cayatceek2006"

locations = ["Ташкент", "Самарканд", "Бухара", "Нукус"]
tariffs = ["Эконом", "Бизнес"]
prices = {"Эконом": 499_900, "Бизнес": 999_900}
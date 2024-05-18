from dataclasses import dataclass
from datetime import date, datetime
from typing import Union


@dataclass
class Flight:
    fid: int
    status: Union[0, 1]
    user_id: int
    location: str
    destination: str
    departure: datetime
    arrival: datetime
    flight: str
    price: int
    tariff: str

    def __str__(self):
        statuses = {0: "Не оплачено", 1: "Оплачено"}
        res = (
            "Информация о полете:\n"
            f"Статус: {statuses[self.status]}\n"
            f"Откуда: {self.location}\n"
            f"Куда: {self.destination}\n"
            f"Время вылета: {self.departure}\n"
            f"Время прибытия: {self.arrival}\n"
            f"Рейс: {self.flight}\n"
            f"Цена: {self.price}\n"
            f"Тариф: {self.tariff}"
            )
        return res
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"status={self.status}, "
            f"user_id={self.user_id}, "
            f"location={self.location}, "
            f"destionation={self.destination}, "
            f"departure={self.departure}, "
            f"arrival={self.arrival}, "
            f"flight={self.flight}, "
            f"price={self.price}, "
            f"tariff={self.tariff}"
            ")>"
        )
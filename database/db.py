import sqlite3
from database.objects import Flight
from datetime import datetime


def create_tables():
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        fid INTEGER PRIMARY KEY,
        status INTEGER,
        user_id INTEGER,
        location TEXT,
        destination TEXT,
        departure TIMESTAMP,
        arrival TIMESTAMP,
        flight TEXT,
        price INTEGER,
        tariff TEXT
    )
    ''')
    con.commit()
    cur.close()
    con.close()

def get_flights_all() -> list[Flight]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM flights')
    res = res.fetchall()
    cur.close()
    con.close()

    flights = []
    for i in res:
        flights.append(Flight(*i))
    
    return flights

def get_flights_by_user_id(user_id: int) -> list[Flight]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM flights WHERE user_id = ? ORDER BY status', (user_id,))
    res = res.fetchall()
    cur.close()
    con.close()

    flights = []
    for i in res:
        flights.append(Flight(*i))
    
    return flights

def get_flight_by_user_id_status(user_id: int, status: int) -> list[Flight]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM flights WHERE user_id = ? AND status = ? ORDER BY status', (user_id, status,))
    res = res.fetchall()
    cur.close()
    con.close()

    flights = []
    for i in res:
        flights.append(Flight(*i))
    
    return flights

def insert_flight(status: int, user_id: int, location: str, destination: str, departure: datetime, arrival: datetime, flight: str, price: int, tariff: str) -> bool:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO flights(status, user_id, location, destination, departure, arrival, flight, price, tariff) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (status, user_id, location, destination, departure, arrival, flight, price, tariff,)
        )
    con.commit()
    cur.close()
    con.close()
    return True

def udate_flight_status(fid: int, status: int) -> bool:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("UPDATE flights SET status = ? WHERE fid = ?", (status, fid,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_flight_by_fid(fid: int) -> bool:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM flights WHERE fid = ?", (fid,))
    is_in_db = res.fetchone()
    if not is_in_db:
        cur.close()
        con.close()
        return False
    cur.execute("DELETE FROM flights WHERE fid = ?", (fid,))
    con.commit()
    cur.close()
    con.close()
    return True
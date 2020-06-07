import sqlite3
import os

# Setting up database
def set_up_database():
    conn = sqlite3.connect("cab_data.sqlite")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS DATA(user_id INTEGER UNIQUE,
                Name TEXT,Phone INTEGER,Age INTEGER,
                City TEXT, Region TEXT, PromoCode TEXT UNIQUE,
                Referral INTEGER, Referral_Points INTEGER)''')
    conn.commit()
    return True


# Returns the list of various columns from the database.
def search(key):
    conn = sqlite3.connect("cab_data.sqlite")
    cur = conn.cursor()
    query = "SELECT " + key + " FROM DATA"
    cur.execute(query)
    li = []
    rows = cur.fetchall()
    for row in rows:
        num = row[0]
        li.append(num)
    conn.commit()
    return li


def save_to_database(data):
    conn = sqlite3.connect("cab_data.sqlite")
    cur = conn.cursor()
    cur.execute('''INSERT INTO DATA(user_id,Name,Phone,Age,City,Region,
    PromoCode,Referral, Referral_Points)VALUES ( ? ,?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['user_id'], data['name'],
          data['phone'], data['age'],
          data['city'], data['region'],
          data['promo_code'], data['referral'],
          data['referral_points']))
    conn.commit()

    return True


def update_referral(promo):
    conn = sqlite3.connect("cab_data.sqlite")
    cur = conn.cursor()
    promo = str(promo)
    query = "UPDATE DATA SET Referral = Referral + 50, Referral_Points = Referral_Points + 1 WHERE user_id = " + promo
    cur.execute(query)
    conn.commit()
    

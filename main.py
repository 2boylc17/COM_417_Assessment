import sqlite3
from Option1 import display

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def start():
    print("What is your shopper ID?")
    shopperid = input()
    sql_query = f"SELECT shopper_id FROM shoppers WHERE shopper_id = {shopperid}"
    cursor.execute(sql_query)
    row = cursor.fetchone()
    if row:
        sql_query = f"SELECT shopper_first_name, shopper_surname FROM shoppers WHERE shopper_id = {row[0]}"
        cursor.execute(sql_query)
        fullname = cursor.fetchone()
        print(f"Welcome {fullname[0]} {fullname[1]}")
        menu(row[0])
    else:
        print("Error: ID does not exist")
        exit()


def menu(sid):
    print(f"\nWhat would you like to do?\n"
          f"[1] - Display your order history\n"
          f"[2] - Add an item to your basket\n"
          f"[3] - View your basket\n"
          f"[4] - Change the quantity of an item from your basket\n"
          f"[5] - Remove an item from your basket\n"
          f"[6] - Checkout\n"
          f"[7] - Exit")
    sql_query = f"SELECT basket_id \
    FROM shopper_baskets \
    WHERE shopper_id = {sid} \
    AND DATE(basket_created_date_time) = DATE('now') \
    ORDER BY basket_created_date_time DESC \
    LIMIT 1"
    cursor.execute(sql_query)
    basket_today = cursor.fetchone()
    print()
    print(f"Your Current Basket:\n {basket_today}")
    num = input()
    if num == '1':
        display(sid)
        menu(sid)
    if num == '7':
        print("Thank you")
        exit()


start()

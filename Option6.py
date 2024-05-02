import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def checkout(basket_id, sid):
    if basket_id is None:
        print("Your basket is empty")
        input()
    else:
        sqlquery = (f"SELECT ROW_NUMBER() OVER(), p.product_description, s.seller_name, b.quantity, \
        PRINTF('£%.2f', b.price), PRINTF('£%.2f', (b.quantity * b.price)) FROM basket_contents b \
                            INNER JOIN products p ON b.product_id = p.product_id \
                            INNER JOIN sellers s ON b.seller_id = s.seller_id WHERE b.basket_id = {basket_id}")
        cursor.execute(sqlquery)
        contents = cursor.fetchall()
        print("{0:<15}{1:70}{2:30}{3:<10}{4:<10}{5:10}".format('Basket Item', 'Product Description',
                                                               'Seller Name', 'Quantity', 'Price', 'Total'))
        overall = 0
        for num in contents:
            row = num[0]
            description = num[1]
            name = num[2]
            quantity = num[3]
            price = num[4]
            total = num[5]
            overall = overall + float(total[1:])
            print('{0:<15}{1:70}{2:30}{3:<10}{4:<10}{5:<10}'.format(row, description, name, quantity, price, total))
        overall = f"£{overall:.2f}"
        print('{0:>143}'.format(overall))
        proceed = input("Would you like to proceed with the checkout? (Y/N) ")
        if proceed == 'Y':
            sql_query = f"SELECT seq+1 FROM sqlite_sequence WHERE name='shopper_orders'"
            cursor.execute(sql_query)
            seq_row = cursor.fetchone()
            sql_insert = f"INSERT INTO shopper_orders VALUES (?,?,DATE('now'),?)"
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(sql_insert, (seq_row[0], sid, 'Placed'))
            sql_query = f"SELECT product_id FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            p_checked = cursor.fetchall()
            sql_query = f"SELECT seller_id FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            s_checked = cursor.fetchall()
            sql_query = f"SELECT quantity FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            q_checked = cursor.fetchall()
            sql_query = f"SELECT price FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            pr_checked = cursor.fetchall()
            for num in range(len(p_checked)):
                sql_query = f"SELECT seq+1 FROM sqlite_sequence WHERE name='shopper_orders'"
                cursor.execute(sql_query)
                seq_row = cursor.fetchone()
                next_id = seq_row[0]
                print(next_id)
                sql_insert = f"INSERT INTO ordered_products VALUES(?,?,?,?,?,'Placed')"
                sql_insert2 = f"INSERT INTO shopper_orders VALUES(?,?,DATE('now'),'Placed')"
                cursor.execute(sql_insert, (next_id, p_checked[num][0], s_checked[num][0], q_checked[num][0], pr_checked[num][0]))
                cursor.execute(sql_insert2, (next_id, sid))
                db.commit()
            sql_query = f"DELETE FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            sql_query = f"DELETE FROM shopper_baskets WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            db.commit()
            input()

        else:
            print("Checkout cancelled")

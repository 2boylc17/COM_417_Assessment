import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def change(basket_id):
    # Checks if there is a basket to be edited
    if basket_id is None:
        print("Your basket is empty")
        input()
    else:
        # Retrieves basket from database
        sqlquery_main = (f"SELECT ROW_NUMBER() OVER(), p.product_description, s.seller_name, b.quantity, \
                            PRINTF('£%.2f', b.price), PRINTF('£%.2f', (b.quantity * b.price)) FROM basket_contents b \
                            INNER JOIN products p ON b.product_id = p.product_id \
                            INNER JOIN sellers s ON b.seller_id = s.seller_id WHERE b.basket_id = {basket_id}")
        cursor.execute(sqlquery_main)
        contents = cursor.fetchall()
        length = len(contents)
        # Checks if there is multiple values in basket
        if length > 1:
            # Prints headers for table
            print("{0:<15}{1:70}{2:30}{3:<10}{4:<10}{5:10}".format('Basket Item', 'Product Description',
                                                                   'Seller Name', 'Quantity', 'Price', 'Total'))
            overall = 0
            # Prints data in table
            for num in contents:
                row = num[0]
                description = num[1]
                name = num[2]
                quantity = num[3]
                price = num[4]
                total = num[5]
                overall = overall + float(total[1:])
                print('{0:<15}{1:70}{2:30}{3:<10}{4:<10}{5:<10}'.format(row, description, name, quantity, price, total))
            # Prints totals of all items added together
            overall = f"£{overall:.2f}"
            print('{0:>143}'.format(overall))
            correct = False
            item_no = 0
            new_quantity = 0
            # Asks the user to enter a basket item number and asks again if the input is invalid
            while correct is False:
                item_no = input("Enter the basket item no. of the item you want to change: ")
                if length < int(item_no) or int(item_no) < 0:
                    print("Error: this item no. is invalid")
                else:
                    correct = True
            correct = False
            # Asks the user to enter the new quantity and asks again if the input is invalid
            while correct is False:
                new_quantity = input("Enter the new quantity of the selected product: ")
                if int(new_quantity) < 1:
                    print("Error: Cannot be below 1")
                else:
                    correct = True
            # Retrieves product IDs
            sql_query = f"SELECT product_id FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            products = cursor.fetchall()
            # Retrieves seller IDs
            sql_query = f"SELECT seller_id FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            sellers = cursor.fetchall()
            r_product = products[int(item_no) - 1][0]
            r_seller = sellers[int(item_no) - 1][0]
            print(r_product, r_seller)
            # Updates basket item to new value
            sql_query = f"UPDATE basket_contents SET quantity = {new_quantity} WHERE basket_id = {basket_id} \
                                                    AND product_id = {r_product} AND seller_id = {r_seller}"
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute(sql_query)
            db.commit()
            cursor.execute(sqlquery_main)
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
            input()
        else:
            # Same process but item_no is always 1
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
            print()
            correct = False
            new_quantity = 0
            item_no = 1
            while correct is False:
                new_quantity = input("Enter the new quantity of the selected product: ")
                if int(new_quantity) < 1:
                    print("Error: Cannot be below 1")
                else:
                    correct = True
            sql_query = f"SELECT product_id FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            products = cursor.fetchall()
            sql_query = f"SELECT seller_id FROM basket_contents WHERE basket_id = {basket_id}"
            cursor.execute(sql_query)
            sellers = cursor.fetchall()
            r_product = products[int(item_no) - 1][0]
            r_seller = sellers[int(item_no) - 1][0]
            print(r_product, r_seller)
            sql_query = f"UPDATE basket_contents SET quantity = {new_quantity} WHERE basket_id = {basket_id} \
                                                    AND product_id = {r_product} AND seller_id = {r_seller}"
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute(sql_query)
            db.commit()
            cursor.execute(sqlquery_main)
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
            input()

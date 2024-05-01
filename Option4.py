import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def change(basket_id):
    if basket_id is None:
        print("Your basket is empty")
        input()
    else:
        sqlquery_main = (f"SELECT ROW_NUMBER() OVER(), p.product_description, s.seller_name, b.quantity, PRINTF('£%.2f', b.price), PRINTF('£%.2f', (b.quantity * b.price)) FROM basket_contents b \
                            INNER JOIN products p ON b.product_id = p.product_id \
                            INNER JOIN sellers s ON b.seller_id = s.seller_id")
        cursor.execute(sqlquery_main)
        contents = cursor.fetchall()
        length = len(contents)
        if length > 1:
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
            overall = f"£{overall}"
            print('{0:>143}'.format(overall))
            print()
            correct = False
            item_no = 0
            new_quantity = 0
            while correct is False:
                item_no = input("Enter the basket item no. of the item you want to change: ")
                if length < int(item_no) or int(item_no) < 0:
                    print("Error: this item no. is invalid")
                else:
                    correct = True
            correct = False
            while correct is False:
                new_quantity = input("Enter the new quantity of the selected product: ")
                if int(new_quantity) < 1:
                    print("Error: Cannot be below 1")
                else:
                    correct = True
            sql_query = f'UPDATE basket_contents SET quantity = {new_quantity} WHERE (SELECT ROW_NUMBER() OVER() FROM basket_contents) = {item_no}'
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
            overall = f"£{overall}"
            print('{0:>143}'.format(overall))
            input()

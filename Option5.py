import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def remove(basket_id):
    if basket_id is None:
        print("Your basket is empty")
        input()
    else:
        sqlquery_main = (f"SELECT ROW_NUMBER() OVER(), p.product_description, s.seller_name, b.quantity, PRINTF('£%.2f', b.price), PRINTF('£%.2f', (b.quantity * b.price)) FROM basket_contents b \
                            INNER JOIN products p ON b.product_id = p.product_id \
                            INNER JOIN sellers s ON b.seller_id = s.seller_id WHERE b.basket_id = {basket_id}")
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
            while correct is False:
                item_no = input("Enter the basket item no. of the item you want to remove: ")
                if length < int(item_no) or int(item_no) < 0:
                    print("Error: this item no. is invalid")
                else:
                    correct = True
            correct = False
            while correct is False:
                dec = input("Would you definitely like to remove this item? (Y/N) ")
                if dec == 'Y':
                    sql_query = f"SELECT product_id FROM basket_contents WHERE basket_id = {basket_id}"
                    cursor.execute(sql_query)
                    products = cursor.fetchall()
                    sql_query = f"SELECT seller_id FROM basket_contents WHERE basket_id = {basket_id}"
                    cursor.execute(sql_query)
                    sellers = cursor.fetchall()
                    r_product = products[int(item_no) - 1][0]
                    r_seller = sellers[int(item_no) - 1][0]
                    sql_query = f"DELETE FROM basket_contents WHERE basket_id = {basket_id} AND product_id = {r_product} AND seller_id = {r_seller}"
                    cursor.execute(sql_query)
                    db.commit()
                    correct = True
                elif dec == 'N':
                    print("Item will not be removed")
                    correct = True
                else:
                    print("Error: this input is invalid")

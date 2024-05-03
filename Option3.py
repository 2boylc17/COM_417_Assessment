import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def display_basket(basket_id):
    # Checks if there is a basket to be displayed
    if basket_id is None:
        print("Your basket is empty")
        input()
    else:
        # Retrieves basket from database
        sqlquery = (f"SELECT ROW_NUMBER() OVER(), p.product_description, s.seller_name, b.quantity, \
                    PRINTF('£%.2f', b.price), PRINTF('£%.2f', (b.quantity * b.price)) FROM basket_contents b \
                    INNER JOIN products p ON b.product_id = p.product_id \
                    INNER JOIN sellers s ON b.seller_id = s.seller_id WHERE b.basket_id = {basket_id}")
        cursor.execute(sqlquery)
        contents = cursor.fetchall()
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
    input()

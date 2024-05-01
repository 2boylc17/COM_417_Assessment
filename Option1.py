import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def display(sid):
    print()
    sql_query = (f"\
        SELECT o.order_id AS [Order ID],\
        STRFTIME('%d-%m-%Y', so.order_date) AS [Order Date],\
        p.product_description AS [Product Description],\
        se.seller_name AS [Seller Name],\
        PRINTF('£%.2f', o.price) AS Price,\
        o.ordered_product_status AS [Order Status]\
    FROM shoppers s\
        INNER JOIN\
        shopper_orders so ON s.shopper_id = so.shopper_id\
        INNER JOIN\
        ordered_products o ON so.order_id = o.order_id\
        INNER JOIN\
        products p ON o.product_id = p.product_id\
        INNER JOIN\
        sellers se ON o.seller_id = se.seller_id\
    WHERE s.shopper_id = {sid}\
    ORDER BY so.order_date DESC;\
    ")
    cursor.execute(sql_query)
    orders = cursor.fetchall()
    if orders:
        print("{0:10}{1:13}{2:80}{3:30}{4:20}{5:10}".format('OrderID', 'Order Date',
                                                           'Product Description', 'Seller', 'Price', 'Qty Status'))
        for num in orders:
            orderid = num[0]
            date = num[1]
            description = num[2]
            seller = num[3]
            price = num[4]
            status = num[5]
            print('{0:<10}{1:13}{2:80}{3:30}{4:20}{5:10}'.format(orderid, date, description, seller, price, status))
    else:
        print("No orders placed by this customer")
    input()

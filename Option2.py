import sqlite3

db = sqlite3.connect('C:/Users/cpboy/Desktop/University/COM 417/parana.db')
cursor = db.cursor()


def _display_options(all_options,title,type):
    option_num = 1
    option_list = []
    print("\n",title,"\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print("{0}.\t{1}".format(option_num, desc))
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the "+type+" you want to choose: "
        selected_option = int(input(prompt))
    return option_list[selected_option - 1]


def add_item(sid, basket):
    print("Which category does the item you intend to purchase fall under?")
    sql_query = f"SELECT category_id, category_description FROM categories"
    cursor.execute(sql_query)
    categories = cursor.fetchall()
    for num in categories:
        categoryid = num[0]
        description = num[1]
        print('{0:<5}{1:5}'.format(categoryid, description))
    cat_chosen = _display_options(categories, 'Categories', 'category')
    sql_query = f"SELECT product_id, product_description FROM products WHERE category_id = {cat_chosen}"
    cursor.execute(sql_query)
    products = cursor.fetchall()
    for num in products:
        productid = num[0]
        product = num[1]
        print('{0:<10}{1:5}'.format(productid, product))
    pro_chosen = _display_options(products, 'Products', 'product')
    sql_query = (f"SELECT s.seller_id, s.seller_name, PRINTF('£%.2f', ps.price) FROM sellers s \
                 INNER JOIN product_sellers ps ON s.seller_id = ps.seller_id WHERE ps.product_id = {pro_chosen}")
    cursor.execute(sql_query)
    sellers = cursor.fetchall()
    for num in sellers:
        sellerid = num[0]
        sellername = num[1]
        price = num[2]
        print('{0:<10}{1:20}{2:5}'.format(sellerid, sellername, price))
    sel_chosen = _display_options(sellers, 'Sellers', 'seller')
    complete = False
    quan_chosen = 0
    while complete is False:
        print("Please enter the quantity of the selected product you wish to purchase (must be greater than 0)")
        quan_chosen = int(input())
        if quan_chosen <= 0:
            print("Error: input not greater than 0")
        else:
            complete = True
    sql_query = f"SELECT price FROM product_sellers WHERE seller_id = {sel_chosen}"
    cursor.execute(sql_query)
    price = cursor.fetchone()
    if basket is None:
        sql_query = f"SELECT seq+1 FROM sqlite_sequence WHERE name='shopper_baskets'"
        cursor.execute(sql_query)
        seq_row = cursor.fetchone()
        next_id = seq_row[0]
        sql_insert = f"INSERT INTO shopper_baskets VALUES(?,?,DATE('now'))"
        cursor.execute(sql_insert, (next_id, sid))
        sql_insert = f"INSERT INTO basket_contents VALUES (?,?,?,?,?)"
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql_insert, (next_id, pro_chosen, sel_chosen, quan_chosen, float(price[0])))
        db.commit()
    else:
        sql_insert = f"INSERT INTO basket_contents VALUES (?,?,?,?,?)"
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql_insert, (basket[0], pro_chosen, sel_chosen, quan_chosen, float(price[0])))
        db.commit()
    print("Item added to your basket")
    input()

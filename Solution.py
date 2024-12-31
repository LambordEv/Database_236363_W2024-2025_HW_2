from typing import List, Tuple
from psycopg2 import sql
from datetime import date, datetime
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish

DEBUG_FLAG = False

# ----------------------- Tables Operations Queries -----------------------
CLEAR_TABLES_QUERY = '''
DELETE FROM Customer;
DELETE FROM Orders;
DELETE FROM Dish;
DELETE FROM Placed;
DELETE FROM OrderedDishes;
DELETE FROM DishRatings;
'''
DROP_TABLES_QUERY = '''
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Dish CASCADE;
DROP TABLE IF EXISTS Placed CASCADE;
DROP TABLE IF EXISTS OrderedDishes CASCADE;
DROP TABLE IF EXISTS DishRatings CASCADE;
'''


CREATE_CUSTOMER_TABLE_QUERY = '''
CREATE TABLE Customer
(
    cust_id INTEGER PRIMARY KEY CHECK (cust_id > 0),
    full_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 120),
    phone TEXT NOT NULL CHECK (LENGTH(phone) = 10)
);
'''

CREATE_ORDER_TABLE_QUERY = '''
CREATE TABLE Orders
(
    order_id INTEGER PRIMARY KEY CHECK (order_id > 0),
    date TIMESTAMP NOT NULL,
    delivery_fee DECIMAL NOT NULL CHECK (delivery_fee >= 0),
    delivery_address TEXT NOT NULL CHECK (LENGTH(delivery_address) >= 5)
);
'''

CREATE_DISH_TABLE_QUERY = '''
CREATE TABLE Dish
(
    dish_id INTEGER PRIMARY KEY CHECK (dish_id > 0),
    name TEXT NOT NULL CHECK (LENGTH(name) >= 4),
    price DECIMAL NOT NULL CHECK (price > 0),
    is_active BOOLEAN NOT NULL
);
'''

CREATE_PLACED_TABLE_QUERY = '''
CREATE TABLE Placed
(
    cust_id INTEGER NOT NULL,
    order_id INTEGER PRIMARY KEY NOT NULL,
    CONSTRAINT fk_cust_id FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE,
    CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    CONSTRAINT unq_order_id UNIQUE (order_id)
);
'''

CREATE_ORDERED_DISHES_TABLE_QUERY = '''
CREATE TABLE OrderedDishes
(
    order_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    dish_amount INTEGER NOT NULL CHECK (dish_amount >= 0),
    dish_price DECIMAL NOT NULL CHECK (dish_price > 0),
    CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_dish_id FOREIGN KEY (dish_id) REFERENCES Dish(dish_id) ON DELETE CASCADE,
    CONSTRAINT unq_dish_order UNIQUE (order_id, dish_id)
);
'''

CREATE_DISH_RATINGS_TABLE_QUERY = '''
CREATE TABLE DishRatings
(
    cust_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (1 <= rating AND rating <= 5),
    CONSTRAINT fk_cust_id FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE,
    CONSTRAINT fk_dish_id FOREIGN KEY (dish_id) REFERENCES Dish(dish_id) ON DELETE CASCADE,
    CONSTRAINT unq_dish_rating UNIQUE (cust_id, dish_id)
);
'''

# ============================== VIEW QUERIES ==============================s
# (Cust_id | [Order_id) | Date | Delivery_Fee | Delivery_Addr | Total_Order_Price}
FULL_ORDER_DETAILS_VIEW = '''
CREATE VIEW FullOrderDetailsView AS
    SELECT 
        p.cust_id AS cust_id,
        o.order_id AS order_id,
        o.date AS order_date,
        o.delivery_fee AS delivery_fee,
        o.delivery_address AS delivery_address,

        SUM(od.dish_amount * od.dish_price) + delivery_fee AS total_order_price
    FROM
        OrderedDishes od
    LEFT JOIN Orders o ON o.order_id = od.order_id
    LEFT JOIN Placed p ON o.order_id = p.order_id
    GROUP BY
        o.order_id, p.cust_id
'''
'''
CREATE VIEW FullOrderDetailsView AS
SELECT 
    o.order_id,
    o.date AS order_date,
    o.delivery_fee,
    o.delivery_address,
    p.cust_id,
    SUM(od.dish_price * od.dish_amount) + o.delivery_fee AS total_order_price
FROM 
    Orders o
LEFT JOIN 
    Placed p ON o.order_id = p.order_id
LEFT JOIN 
    OrderedDishes od ON o.order_id = od.order_id
GROUP BY 
    o.order_id, o.date, o.delivery_fee, o.delivery_address, p.cust_id;
'''
# ============================== VIEW QUERIES ==============================s


# in case of an illegal or a failed database communication
def handle_database_exceptions(query: sql.SQL, e: Exception, print_flag = False) -> ReturnValue:
    result = ReturnValue.ERROR
    if print_flag:
        print('Database Raised An Exception!')
        print(f'The Query that is responsible for the exception - {query}')
        print(e)

    if isinstance(e, DatabaseException.NOT_NULL_VIOLATION):
        result = ReturnValue.BAD_PARAMS
    elif isinstance(e, DatabaseException.CHECK_VIOLATION):
        result = ReturnValue.BAD_PARAMS
    elif isinstance(e, DatabaseException.FOREIGN_KEY_VIOLATION):
        result = ReturnValue.NOT_EXISTS
    elif isinstance(e, DatabaseException.UNIQUE_VIOLATION):
        result = ReturnValue.ALREADY_EXISTS
    elif isinstance(e, DatabaseException.ConnectionInvalid):
        result = ReturnValue.ERROR
    elif isinstance(e, DatabaseException.UNKNOWN_ERROR):
        result = ReturnValue.ERROR

    return result


def handle_query_insertion(query: sql.SQL) -> Tuple[ReturnValue, int]:
    query_result = ReturnValue.ERROR
    rows_amount = -1
    conn = Connector.DBConnector()
    try:
        rows_amount, _ = conn.execute(query)
        conn.commit()
        query_result = ReturnValue.OK
    except Exception as e:
        query_result = handle_database_exceptions(query, e, DEBUG_FLAG)
    finally:
        conn.close()
    return query_result, rows_amount


def handle_query_selection(query: sql.SQL) -> Tuple[ReturnValue, int, Connector.ResultSet]:
    conn = Connector.DBConnector()
    query_result = (ReturnValue.ERROR, -1, None)
    try:
        rows_amount, data = conn.execute(query)
        query_result = (ReturnValue.OK, rows_amount, data)
        conn.commit()
    except Exception as e:
        exception_result = handle_database_exceptions(query, e)
        query_result = (exception_result, -1, None)
    finally:
        conn.close()

    return query_result


def handle_query_deletion(query: sql.SQL) -> ReturnValue:
    query_result = ReturnValue.ERROR
    conn = Connector.DBConnector()
    try:
        rows_amount, data_deleted = conn.execute(query)
        conn.commit()
        if 0 == rows_amount:
            query_result = ReturnValue.NOT_EXISTS
        elif 1 < rows_amount:
            if DEBUG_FLAG:
                print(f'Something went wrong on deletion!\n'
                      f'Deleted {rows_amount} rows - possible meaning UNIQUE VIOLATION!')
            query_result = ReturnValue.ERROR
        else:
            query_result = ReturnValue.OK
    except Exception as e:
        query_result = handle_database_exceptions(query, e, DEBUG_FLAG)
    finally:
        conn.close()

    return query_result


# ---------------------------------- CRUD API: ----------------------------------
# Basic database functions

def create_tables() -> None:
    conn = None
    # Tables Creation
    query = CREATE_CUSTOMER_TABLE_QUERY + \
            CREATE_ORDER_TABLE_QUERY + \
            CREATE_DISH_TABLE_QUERY + \
            CREATE_PLACED_TABLE_QUERY + \
            CREATE_ORDERED_DISHES_TABLE_QUERY + \
            CREATE_DISH_RATINGS_TABLE_QUERY
    # Views Creation
    query += FULL_ORDER_DETAILS_VIEW

    try:
        conn = Connector.DBConnector()
        query = sql.SQL(query)
        conn.execute(query)
        conn.commit()

    except Exception as e:
        handle_database_exceptions(query, e, DEBUG_FLAG)
    finally:
        conn.close()


def clear_tables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(CLEAR_TABLES_QUERY)
        conn.execute(query)
        conn.commit()

    except Exception as e:
        handle_database_exceptions(query, e, DEBUG_FLAG)
    finally:
        conn.close()


def drop_tables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(DROP_TABLES_QUERY)
        conn.execute(query)
        conn.commit()

    except Exception as e:
        handle_database_exceptions(query, e, DEBUG_FLAG)
    finally:
        conn.close()


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    ADD_CUSTOMER_QUERY_FORMAT = '''
        INSERT INTO Customer(cust_id, full_name, age, phone)
        VALUES({cust_id}, {full_name}, {age}, {phone})
    '''

    query = sql.SQL(ADD_CUSTOMER_QUERY_FORMAT).format(
        cust_id = sql.Literal(customer.get_cust_id()),
        full_name = sql.Literal(customer.get_full_name()),
        age = sql.Literal(customer.get_age()),
        phone = sql.Literal(customer.get_phone())
    )

    ret_val, _ = handle_query_insertion(query)

    return ret_val


def get_customer(customer_id: int) -> Customer:
    GET_CUSTOMER_QUERY_FORMAT = '''
        SELECT * FROM Customer WHERE cust_id={cust_id}
    '''
    result = BadCustomer()

    query = sql.SQL(GET_CUSTOMER_QUERY_FORMAT).format(
        cust_id = sql.Literal(customer_id)
    )

    _, rows_effected, rows = handle_query_selection(query)
    if 1 == rows_effected:
        result = Customer(rows[0]['cust_id'], rows[0]['full_name'], rows[0]['age'], rows[0]['phone'])

    return result


def delete_customer(customer_id: int) -> ReturnValue:
    DELETE_CUSTOMER_QUERY_FORMAT = '''
        DELETE FROM Customer WHERE cust_id={cust_id}
    '''

    query = sql.SQL(DELETE_CUSTOMER_QUERY_FORMAT).format(
        cust_id = sql.Literal(customer_id)
    )
    ret_val = handle_query_deletion(query)

    return ret_val


def add_order(order: Order) -> ReturnValue:
    ADD_ORDER_QUERY_FORMAT = '''
        INSERT INTO Orders(order_id, date, delivery_fee, delivery_address)
        VALUES({order_id}, {date}, {delivery_fee}, {delivery_address})
    '''

    query = sql.SQL(ADD_ORDER_QUERY_FORMAT).format(
        order_id = sql.Literal(order.get_order_id()),
        date = sql.Literal(order.get_datetime()),
        delivery_fee = sql.Literal(order.get_delivery_fee()),
        delivery_address = sql.Literal(order.get_delivery_address())
    )

    ret_val, _ = handle_query_insertion(query)

    return ret_val


def get_order(order_id: int) -> Order:
    GET_ORDER_QUERY_FORMAT = '''
        SELECT * FROM Orders WHERE order_id={order_id}
    '''
    result = BadOrder()

    query = sql.SQL(GET_ORDER_QUERY_FORMAT).format(
        order_id = sql.Literal(order_id)
    )

    _, rows_effected, rows = handle_query_selection(query)
    if 1 == rows_effected:
        result = Order(rows[0]['order_id'], rows[0]['date'], rows[0]['delivery_fee'], rows[0]['delivery_address'])

    return result


def delete_order(order_id: int) -> ReturnValue:
    DELETE_ORDER_QUERY_FORMAT = '''
        DELETE FROM Orders WHERE order_id={order_id}
    '''

    query = sql.SQL(DELETE_ORDER_QUERY_FORMAT).format(
        order_id = sql.Literal(order_id)
    )
    ret_val = handle_query_deletion(query)

    return ret_val


def add_dish(dish: Dish) -> ReturnValue:
    ADD_DISH_QUERY_FORMAT = '''
        INSERT INTO Dish(dish_id, name, price, is_active)
        VALUES({dish_id}, {name}, {price}, {is_active})
    '''

    query = sql.SQL(ADD_DISH_QUERY_FORMAT).format(
        dish_id = sql.Literal(dish.get_dish_id()),
        name = sql.Literal(dish.get_name()),
        price = sql.Literal(dish.get_price()),
        is_active = sql.Literal(dish.get_is_active())
    )

    ret_val, _ = handle_query_insertion(query)

    return ret_val


def get_dish(dish_id: int) -> Dish:
    GET_DISH_QUERY_FORMAT = '''
        SELECT * FROM Dish WHERE dish_id={dish_id}
    '''
    result = BadDish()

    query = sql.SQL(GET_DISH_QUERY_FORMAT).format(
        dish_id = sql.Literal(dish_id)
    )

    _, rows_effected, rows = handle_query_selection(query)
    if 1 == rows_effected:
        result = Dish(rows[0]['dish_id'], rows[0]['name'], rows[0]['price'], rows[0]['is_active'])

    return result


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    result = ReturnValue.ERROR
    UPDATE_DISH_PRICE_QUERY_FORMAT = '''
        UPDATE Dish SET price = {price} WHERE (dish_id={dish_id} AND is_active=TRUE)
    '''

    query = sql.SQL(UPDATE_DISH_PRICE_QUERY_FORMAT).format(
        dish_id = sql.Literal(dish_id),
        price = sql.Literal(price)
    )
    result, rows_updated = handle_query_insertion(query)
    if ReturnValue.OK == result and 0 == rows_updated:
        # (Evgeny) - As I understand this is the case when we are trying "Change the price of an un-active dish"
        result = ReturnValue.NOT_EXISTS

    return result


def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    result = ReturnValue.ERROR
    UPDATE_DISH_PRICE_QUERY_FORMAT = '''
            UPDATE Dish SET is_active = {is_active} WHERE dish_id={dish_id}
        '''

    query = sql.SQL(UPDATE_DISH_PRICE_QUERY_FORMAT).format(
        dish_id = sql.Literal(dish_id),
        is_active = sql.Literal(is_active)
    )
    result, rows_updated = handle_query_insertion(query)
    if ReturnValue.OK == result and 0 == rows_updated:
        # (Evgeny) - As I understand this is the case when we are trying "Change the status of a 'non-existing in the system' dish"
        result = ReturnValue.NOT_EXISTS

    return result


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    result = ReturnValue.ERROR
    CUSTOMER_PLACED_ORDER_QUERY_FORMAT = '''
        INSERT INTO Placed(cust_id, order_id)
        VALUES({cust_id}, {order_id})
    '''

    query = sql.SQL(CUSTOMER_PLACED_ORDER_QUERY_FORMAT).format(
        cust_id=sql.Literal(customer_id),
        order_id=sql.Literal(order_id)
    )
    ret_val, _ = handle_query_insertion(query)

    return ret_val


def get_customer_that_placed_order(order_id: int) -> Customer:
    GET_CUSTOMER_THAT_PLACED_ORDER_QUERY = '''
        SELECT * FROM Customer WHERE cust_id = (SELECT cust_id FROM Placed WHERE order_id = {order_id})
    '''
    query = sql.SQL(GET_CUSTOMER_THAT_PLACED_ORDER_QUERY).format(
        order_id = sql.Literal(order_id)
    )

    retval = BadCustomer()
    result, rows_amount, data = handle_query_selection(query)
    if 1 == rows_amount:
        retval = Customer(data[0]['cust_id'], data[0]['full_name'], data[0]['age'], data[0]['phone'])

    return retval



def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    ORDER_CONTAIN_DISH_QUERY_FORMAT = '''
        INSERT INTO OrderedDishes(order_id, dish_id, dish_amount, dish_price)
        VALUES(
            {order_id}, 
            {dish_id}, 
            {amount}, 
            (SELECT price FROM Dish WHERE (dish_id = {dish_id} AND is_active = TRUE))
        )
    '''
    query = sql.SQL(ORDER_CONTAIN_DISH_QUERY_FORMAT).format(
        order_id = sql.Literal(order_id),
        dish_id = sql.Literal(dish_id),
        amount = sql.Literal(amount)
    )
    ret_val, rows_inserted = handle_query_insertion(query)
    if ReturnValue.BAD_PARAMS == ret_val and order_id > 0 and dish_id > 0 and amount >= 0:
        # (Evgeny) - As I understand this is the case when we are trying "Adding a dish to an order while the dish is not active"
        ret_val = ReturnValue.NOT_EXISTS

    return ret_val


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    DELETE_ORDER_QUERY_FORMAT = '''
        DELETE FROM OrderedDishes WHERE (order_id={order_id} AND dish_id={dish_id})
    '''

    query = sql.SQL(DELETE_ORDER_QUERY_FORMAT).format(
        order_id=sql.Literal(order_id),
        dish_id=sql.Literal(dish_id)
    )
    ret_val = handle_query_deletion(query)

    return ret_val


def get_all_order_items(order_id: int) -> List[OrderDish]:
    GET_ALL_ORDERED_ITEMS_QUERY = '''
        SELECT * FROM OrderedDishes WHERE order_id = {order_id}
    '''
    query = sql.SQL(GET_ALL_ORDERED_ITEMS_QUERY).format(
        order_id=sql.Literal(order_id)
    )

    result, rows_amount, data = handle_query_selection(query)
    retval = [OrderDish(row['dish_id'], row['dish_amount'], row['dish_price']) for row in data]

    return retval


def customer_rated_dish(cust_id: int, dish_id: int, rating: int) -> ReturnValue:
    CUSTOMER_DISH_RATE_QUERY_FORMAT = '''
        INSERT INTO DishRatings(cust_id, dish_id, rating)
        VALUES(
            {cust_id}, 
            {dish_id}, 
            {rating} 
        )
    '''
    query = sql.SQL(CUSTOMER_DISH_RATE_QUERY_FORMAT).format(
        cust_id=sql.Literal(cust_id),
        dish_id=sql.Literal(dish_id),
        rating=sql.Literal(rating)
    )
    ret_val, _ = handle_query_insertion(query)

    return ret_val


def customer_deleted_rating_on_dish(cust_id: int, dish_id: int) -> ReturnValue:
    DELETE_DISH_RATING_QUERY_FORMAT = '''
        DELETE FROM DishRatings WHERE (cust_id={cust_id} AND dish_id={dish_id})
    '''

    query = sql.SQL(DELETE_DISH_RATING_QUERY_FORMAT).format(
        cust_id=sql.Literal(cust_id),
        dish_id=sql.Literal(dish_id)
    )
    ret_val = handle_query_deletion(query)

    return ret_val


def get_all_customer_ratings(cust_id: int) -> List[Tuple[int, int]]:
    GET_ALL_CUSTOMER_RATINGS_QUERY_FORMAT = '''
        SELECT * FROM DishRatings WHERE cust_id = {cust_id} ORDER BY dish_id ASC
    '''
    query = sql.SQL(GET_ALL_CUSTOMER_RATINGS_QUERY_FORMAT).format(
        cust_id=sql.Literal(cust_id)
    )

    result, rows_amount, data = handle_query_selection(query)
    retval = [(row['dish_id'], row['rating']) for row in data]

    return retval


# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    GET_ORDER_TOTAL_PRICE_QUERY_FORMAT = '''
        SELECT * FROM FullOrderDetailsView 
        WHERE order_id = {order_id}; 
    '''
    query = sql.SQL(GET_ORDER_TOTAL_PRICE_QUERY_FORMAT).format(
        order_id = sql.Literal(order_id)
    )

    result, rows_amount, data = handle_query_selection(query)

    return float(data[0]['total_order_price'])


def get_customers_spent_max_avg_amount_money() -> List[int]:
    GET_CUSTOMER_MAX_AVG_QUERY = '''
        WITH tmp_avg_price AS (
            SELECT cust_id, AVG(total_order_price) AS avg_price FROM FullOrderDetailsView
            GROUP BY cust_id
        )
        SELECT cust_id FROM tmp_avg_price
        WHERE avg_price = (SELECT MAX(avg_price) FROM tmp_avg_price)
        ORDER BY cust_id ASC; 
    '''
    query = sql.SQL(GET_CUSTOMER_MAX_AVG_QUERY)
    result, rows_amount, data = handle_query_selection(query)

    return [row['cust_id'] for row in data]


def get_most_purchased_dish_among_anonymous_order() -> Dish:
    # TODO: implement
    pass


def did_customer_order_top_rated_dishes(cust_id: int) -> bool:
    # TODO: implement
    pass


# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API


def get_customers_rated_but_not_ordered() -> List[int]:
    # TODO: implement
    pass


def get_non_worth_price_increase() -> List[int]:
    # TODO: implement
    pass


def get_cumulative_profit_per_month(year: int) -> List[Tuple[int, float]]:
    # TODO: implement
    pass


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    # TODO: implement
    pass

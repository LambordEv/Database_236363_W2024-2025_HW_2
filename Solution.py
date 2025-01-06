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
from datetime import datetime

DEBUG_FLAG = False

# ----------------------------- QUERY TABLE DEFINITION: -----------------------------

#object tables
CREATE_CUSTOMER_TABLE_QUERY = '''
CREATE TABLE Customer
(
    cust_id     INTEGER     NOT NULL,
    full_name   TEXT        NOT NULL,
    age         INTEGER     NOT NULL,
    phone       VARCHAR(10) NOT NULL,
    PRIMARY KEY (cust_id),
    CHECK       (cust_id > 0),
    CHECK       (age >= 18  AND age <= 120),
    CHECK       (LENGTH(phone) = 10)
);
'''

CREATE_ORDER_TABLE_QUERY = '''
CREATE TABLE Orders
(
    order_id            INTEGER                         NOT NULL,        
    date                TIMESTAMP(0) WITHOUT TIME ZONE  NOT NULL,
    delivery_fee        DECIMAL                         NOT NULL,      
    delivery_address    TEXT                            NOT NULL,
    PRIMARY KEY         (order_id),    
    CHECK               (order_id > 0),
    CHECK               (delivery_fee > 0),
    CHECK               (LENGTH(delivery_address) >= 5)
);
'''

CREATE_DISH_TABLE_QUERY = '''
CREATE TABLE Dish
(
    dish_id     INTEGER  NOT NULL,
    name        TEXT     NOT NULL,
    price       DECIMAL  NOT NULL, 
    is_active   BOOLEAN  NOT NULL,
    PRIMARY KEY         (dish_id),
    CHECK               (dish_id  > 0),
    CHECK               (price  > 0),
    CHECK               (LENGTH(name) >= 4)
);
'''

#relation tables
CREATE_PLACED_TABLE_QUERY = '''
CREATE TABLE Placed
(
    order_id    INTEGER NOT NULL,
    cust_id     INTEGER NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (cust_id)  REFERENCES Customer(cust_id) ON DELETE CASCADE
);
'''


CREATE_ORDERED_DISHES_TABLE_QUERY = '''
CREATE TABLE OrderedDishes
(
    order_id        INTEGER     NOT NULL,
    dish_id         INTEGER     NOT NULL,
    dish_price      DECIMAL     NOT NULL,
    dish_amount     INTEGER     NOT NULL,
    PRIMARY KEY     (order_id,  dish_id), 
    FOREIGN KEY     (order_id)  REFERENCES  Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY     (dish_id)   REFERENCES  Dish(dish_id), 
    CHECK           (dish_price > 0),
    CHECK           (dish_amount > 0)    
);
'''
CREATE_DISH_RATINGS_TABLE_QUERY = '''
CREATE TABLE DishRatings
(
    cust_id     INTEGER     NOT NULL, 
    dish_id     INTEGER     NOT NULL,
    rating      INTEGER     NOT NULL,
    PRIMARY KEY (cust_id,  dish_id), 
    FOREIGN KEY (cust_id)  REFERENCES   Customer(cust_id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id)   REFERENCES  Dish(dish_id),
    CHECK       (rating > 0 AND rating <= 5)
);
'''

# ------------------------------- Database Views Definitions -------------------------------
CREATE_VIEW_ORDERSSUM = '''
CREATE VIEW OrdersSum AS
(
    SELECT Orders.order_id AS order_id,
           COALESCE(SUM(OrderedDishes.dish_price * OrderedDishes.dish_amount),0) AS total,
            MAX(Orders.delivery_fee) AS delivery_fee
    FROM Orders LEFT OUTER JOIN OrderedDishes
        ON Orders.order_id = OrderedDishes.order_id
    GROUP BY Orders.order_id
);   
'''

CREATE_VIEW_CUSTOMESRORDERS = '''
CREATE VIEW CustomersOrders AS
(
    SELECT  Placed.cust_id AS cust_id, 
            Orders.order_id AS order_id
    FROM Orders
    LEFT JOIN Placed ON Orders.order_id = Placed.order_id
);
'''


CREATE_VIEW_RATINGSCORE = '''
CREATE VIEW RatingScore AS
(
    SELECT Dish.dish_id AS dish_id, COALESCE(AVG(DishRatings.rating), 3) AS avg_rating
    FROM Dish LEFT OUTER JOIN DishRatings ON (Dish.dish_id = DishRatings.dish_id)
    GROUP BY Dish.dish_id
);       
'''


CREATE_VIEW_APPO= '''
CREATE VIEW appo AS
(
    SELECT dish_id , dish_price , COALESCE(AVG(dish_amount), 0)*dish_price AS val 
    FROM OrderedDishes
    GROUP BY dish_id , dish_price
);
'''
CREATE_VIEW_ORDERED_DISHES_BY_CUSTOMER = '''
CREATE VIEW CustomerOrderedDishes AS
(
    SELECT p.cust_id, od.dish_id FROM
    OrderedDishes od JOIN Placed p ON (p.order_id = od.order_id)
);
'''

CREATE_VIEW_SIMILAR_RELATION = '''
CREATE VIEW SimilarRelation AS
(
    SELECT dr1.cust_id AS a, dr2.cust_id AS b FROM
    DishRatings dr1 JOIN DishRatings dr2 ON dr1.dish_id = dr2.dish_id
    WHERE dr1.cust_id != dr2.cust_id AND
          dr1.rating >= 4 AND dr2.rating >= 4
);
'''

All_TABLE_NAMES = ['DishRatings', 'OrderedDishes', 'Placed', 'Orders', 'Dish', 'Customer']
ALL_VIEW_NAMES = ['OrdersSum', 'CustomersOrders', 'RatingScore', 'appo', 'CustomerOrderedDishes', 'SimilarRelation']


# ------------------------------- Function helper: -------------------------------
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
    elif isinstance(e, DatabaseException.database_ini_ERROR):
        result = ReturnValue.ERROR        

    return result


def handle_query(query: sql.SQL) -> Tuple[ReturnValue, int, Connector.ResultSet, Exception]:
    query_result = ReturnValue.OK
    rows_amount = 0
    result = None
    recieved_exp = None
    conn = Connector.DBConnector()

    try:
        rows_amount, result = conn.execute(query)
        conn.commit()
    except Exception as e:
        recieved_exp = e
        query_result = handle_database_exceptions(query, e, DEBUG_FLAG)
    finally:
        conn.close()

    return query_result, rows_amount, result, recieved_exp


def return_Value_select(qstatus:ReturnValue, rows_effected)-> ReturnValue:
        if qstatus == ReturnValue.OK and rows_effected == 0:
            return ReturnValue.NOT_EXISTS
        return qstatus

# ---------------------------------- CRUD API: ----------------------------------
# Basic database functions

def create_tables() -> None:
    conn = None
    # Tables Creation
    CREATE_TABLES_QUERY_FORMAT = CREATE_CUSTOMER_TABLE_QUERY + \
            CREATE_ORDER_TABLE_QUERY + \
            CREATE_DISH_TABLE_QUERY + \
            CREATE_PLACED_TABLE_QUERY + \
            CREATE_ORDERED_DISHES_TABLE_QUERY  + \
            CREATE_DISH_RATINGS_TABLE_QUERY + \
            CREATE_VIEW_ORDERSSUM + \
            CREATE_VIEW_CUSTOMESRORDERS + \
            CREATE_VIEW_RATINGSCORE + \
            CREATE_VIEW_APPO + \
            CREATE_VIEW_SIMILAR_RELATION + \
            CREATE_VIEW_ORDERED_DISHES_BY_CUSTOMER

    query = sql.SQL(CREATE_TABLES_QUERY_FORMAT)
    _, _, _, exp = handle_query(query)


def clear_tables() -> None:
    CLEAR_TABLES_QUERY_FORMAT = '\n'.join([f"DELETE FROM {table};" for table in All_TABLE_NAMES])
    query = sql.SQL(CLEAR_TABLES_QUERY_FORMAT)
    handle_query(query)


def drop_tables() -> None:
    DROP_TABLES_AND_VIEWS_QUERY_FORMAT = '\n'.join([f"DROP VIEW IF EXISTS {table};" for table in ALL_VIEW_NAMES])
    DROP_TABLES_AND_VIEWS_QUERY_FORMAT += '\n'.join([f"DROP TABLE IF EXISTS {table} CASCADE;" for table in All_TABLE_NAMES])
    query = sql.SQL(DROP_TABLES_AND_VIEWS_QUERY_FORMAT)
    handle_query(query)
    


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    ADD_CUSTOMER_QUERY_FORMAT = '''
        INSERT INTO Customer(cust_id,full_name,age,phone)
        VALUES({cust_id}, {full_name}, {age}, {phone})
    '''  
    query = sql.SQL(ADD_CUSTOMER_QUERY_FORMAT).format(
        cust_id = sql.Literal(customer.get_cust_id()),
        full_name = sql.Literal(customer.get_full_name()),
        age = sql.Literal(customer.get_age()),
        phone = sql.Literal(customer.get_phone())
    )

    q_status, _, _, _ = handle_query(query)
    return q_status



def get_customer(customer_id: int) -> Customer:
    GET_CUSTOMER_QUERY_FORMAT = f'''
        SELECT * FROM Customer WHERE cust_id={customer_id}
    '''
    query = sql.SQL(GET_CUSTOMER_QUERY_FORMAT)
    qstatus, rows_effected, rows, _ = handle_query(query)
    qstatus = return_Value_select(qstatus,rows_effected)
   
    if qstatus != ReturnValue.OK:
        retObject = BadCustomer()
    else:
        retObject = Customer(rows[0]['cust_id'], rows[0]['full_name'], rows[0]['age'], rows[0]['phone'])
    return retObject


def delete_customer(customer_id: int) -> ReturnValue:
    DELETE_CUSTOMER_QUERY_FORMAT = f'''
        DELETE FROM Customer WHERE cust_id={customer_id}
    '''
    query = sql.SQL(DELETE_CUSTOMER_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    return return_Value_select(qstatus, rows_effected)


def add_order(order: Order) -> ReturnValue:
    # TODO- order.get_datetime() should be in secend ?
    ADD_ORDER_QUERY_FORMAT = '''
        INSERT INTO Orders(order_id, date, delivery_fee, delivery_address)
        VALUES({order_id}, {date}, {delivery_fee}, {delivery_address})
    '''
    query = sql.SQL(ADD_ORDER_QUERY_FORMAT).format(
        order_id = sql.Literal(order.get_order_id()),
        date = sql.Literal(order.get_datetime().strftime("%Y-%m-%d %H:%M:%S")),
        delivery_fee = sql.Literal(order.get_delivery_fee()),
        delivery_address = sql.Literal(order.get_delivery_address())
    )
    q_status, _, _, _ = handle_query(query)
    return q_status


def get_order(order_id: int) -> Order:
    GET_ORDER_QUERY_FORMAT = f'''
        SELECT * FROM Orders WHERE order_id={order_id}
    '''
    query = sql.SQL(GET_ORDER_QUERY_FORMAT)
    qstatus, rows_effected, rows, _ = handle_query(query)
    qstatus = return_Value_select(qstatus, rows_effected)
    if qstatus != ReturnValue.OK:
        retObject = BadOrder()
    else:
        retObject = Order(rows[0]['order_id'], rows[0]['date'], rows[0]['delivery_fee'], rows[0]['delivery_address'])
    return retObject    



def delete_order(order_id: int) -> ReturnValue:
    DELETE_ORDER_QUERY_FORMAT = f'''
    DELETE FROM Orders WHERE order_id={order_id}
    '''
    query = sql.SQL(DELETE_ORDER_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    return return_Value_select(qstatus, rows_effected)


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
    qstatus, rows_effected, _, _ = handle_query(query)
    return qstatus

def get_dish(dish_id: int) -> Dish:
    GET_DISH_QUERY_FORMAT = f'''
        SELECT * FROM Dish WHERE dish_id={dish_id}
    '''
    retObject = BadDish()
    query = sql.SQL(GET_DISH_QUERY_FORMAT)
    qstatus, rows_effected, rows, _ = handle_query(query)
    qstatus = return_Value_select(qstatus, rows_effected)

    if qstatus == ReturnValue.OK:
        retObject = Dish(rows[0]['dish_id'], rows[0]['name'], rows[0]['price'], rows[0]['is_active'])
    return retObject


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    UPDATE_DISH_PRICE_QUERY_FORMAT = f'''
        UPDATE Dish SET price = {price} WHERE (dish_id={dish_id} AND is_active=TRUE)
    '''
    query = sql.SQL(UPDATE_DISH_PRICE_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    if ReturnValue.OK == qstatus and 0 == rows_effected:
        qstatus = ReturnValue.NOT_EXISTS
    return  qstatus

def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    UPDATE_DISH_PRICE_QUERY_FORMAT = f'''
        UPDATE Dish SET is_active = {is_active} WHERE dish_id={dish_id}
    '''
    query = sql.SQL(UPDATE_DISH_PRICE_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    if ReturnValue.OK == qstatus and 0 == rows_effected:
        qstatus = ReturnValue.NOT_EXISTS
    return qstatus


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    CUSTOMER_PLACED_ORDER_QUERY_FORMAT = f'''
        INSERT INTO Placed(cust_id, order_id)
        VALUES({customer_id}, {order_id})
    '''
    query = sql.SQL(CUSTOMER_PLACED_ORDER_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    return qstatus

def get_customer_that_placed_order(order_id: int) -> Customer:
    GET_CUSTOMER_THAT_PLACED_ORDER_QUERY = f'''
        SELECT * FROM Customer WHERE cust_id = (SELECT cust_id FROM Placed WHERE order_id = {order_id})
    '''
    retObject = BadCustomer()
    query = sql.SQL(GET_CUSTOMER_THAT_PLACED_ORDER_QUERY)
    qstatus, rows_effected, data, _ = handle_query(query)
    qstatus = return_Value_select(qstatus,rows_effected)
    if ReturnValue.OK == qstatus:
        retObject = Customer(data[0]['cust_id'], data[0]['full_name'], data[0]['age'], data[0]['phone'])
    return retObject    

def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    ORDER_CONTAIN_DISH_QUERY_FORMAT = f'''
        INSERT INTO OrderedDishes(order_id, dish_id, dish_amount, dish_price)
        VALUES({order_id}, {dish_id}, {amount}, 
            (SELECT price FROM Dish WHERE (dish_id = {dish_id} AND is_active = TRUE))
        )
    '''
    query = sql.SQL(ORDER_CONTAIN_DISH_QUERY_FORMAT)
    qstatus, rows_effected, _, exp = handle_query(query)
    if isinstance(exp, DatabaseException.NOT_NULL_VIOLATION):
        qstatus = ReturnValue.NOT_EXISTS
    return qstatus


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    DELETE_ORDER_QUERY_FORMAT = f'''
        DELETE FROM OrderedDishes WHERE (order_id={order_id} AND dish_id={dish_id})
    '''
    query = sql.SQL(DELETE_ORDER_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    return return_Value_select(qstatus,rows_effected)

def get_all_order_items(order_id: int) -> List[OrderDish]:
    GET_ALL_ORDERED_ITEMS_QUERY = f'''
        SELECT * FROM OrderedDishes 
        WHERE order_id = {order_id}
        ORDER BY dish_id ASC
    '''
    retObject = []
    query = sql.SQL(GET_ALL_ORDERED_ITEMS_QUERY)
    qstatus, rows_effected, data, _ = handle_query(query)
    qstatus = return_Value_select(qstatus,rows_effected)
    if ReturnValue.OK == qstatus:
        retObject = [OrderDish(row['dish_id'], row['dish_amount'], row['dish_price']) for row in data]
    
    return retObject 


def customer_rated_dish(cust_id: int, dish_id: int, rating: int) -> ReturnValue:
    CUSTOMER_DISH_RATE_QUERY_FORMAT = f'''
        INSERT INTO DishRatings(cust_id, dish_id, rating)
        VALUES({cust_id}, {dish_id}, {rating} 
        )
    '''
    query = sql.SQL(CUSTOMER_DISH_RATE_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    return qstatus
    

def customer_deleted_rating_on_dish(cust_id: int, dish_id: int) -> ReturnValue:
    DELETE_DISH_RATING_QUERY_FORMAT = f'''
        DELETE FROM DishRatings WHERE (cust_id={cust_id} AND dish_id={dish_id})
    '''
    query = sql.SQL(DELETE_DISH_RATING_QUERY_FORMAT)
    qstatus, rows_effected, _, _ = handle_query(query)
    return return_Value_select(qstatus, rows_effected)

def get_all_customer_ratings(cust_id: int) -> List[Tuple[int, int]]:
    GET_ALL_CUSTOMER_RATINGS_QUERY_FORMAT = f'''
        SELECT * FROM DishRatings WHERE cust_id = {cust_id} ORDER BY dish_id ASC
    '''
    retObject = []
    query = sql.SQL(GET_ALL_CUSTOMER_RATINGS_QUERY_FORMAT)
    qstatus, rows_effected, data, _ = handle_query(query)
    qstatus = return_Value_select(qstatus, rows_effected)
    if ReturnValue.OK == qstatus:
        retObject = [(row['dish_id'], row['rating']) for row in data]
    return retObject     
# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    GET_ORDER_TOTAL_PRICE_QUERY_FORMAT = f'''
        SELECT total+delivery_fee AS pay
        FROM OrdersSum
        WHERE OrdersSum.order_id = {order_id}
        LIMIT 1
    '''
    query = sql.SQL(GET_ORDER_TOTAL_PRICE_QUERY_FORMAT)
    _, _, data, _ = handle_query(query)
    return float(data[0]['pay'])


def get_customers_spent_max_avg_amount_money() -> List[int]:
    #:including dekiveryfee see in oazzza @34
    GET_CUSTOMERS_SPENT_MAX_AVG_AMOUNT_MONY_QUERY_FORMAT = '''
        SELECT Co.cust_id
        FROM CustomersOrders AS Co JOIN OrdersSum AS Os ON(Co.order_id = Os.order_id)
        WHERE Co.cust_id IS NOT NULL
        GROUP BY Co.cust_id
        HAVING  SUM(Os.total + Os.delivery_fee)/COALESCE(COUNT(*),1) = (
                    SELECT  sum(OrdersSum.total + OrdersSum.delivery_fee)/COALESCE(COUNT(*),1) max
                    FROM CustomersOrders JOIN OrdersSum ON(CustomersOrders.order_id = OrdersSum.order_id)
                    WHERE  CustomersOrders.cust_id IS NOT NULL 
                    GROUP BY CustomersOrders.cust_id                      
                    ORDER BY SUM(OrdersSum.total + OrdersSum.delivery_fee)/COALESCE(COUNT(*),1) DESC
                    LIMIT 1 )
        ORDER BY Co.cust_id ASC
    ''' 
    query = sql.SQL(GET_CUSTOMERS_SPENT_MAX_AVG_AMOUNT_MONY_QUERY_FORMAT)
    _, _, data, _ = handle_query(query)
    if data is None:
        return []
    return [row['cust_id'] for row in data]


def get_most_purchased_dish_among_anonymous_order() -> Dish:
    GET_MOST_PURCHASED_DISH_AMONG_ANONYMOUS_QUERY_FORMAT = '''
    SELECT *
    FROM Dish
    WHERE dish_id =(
        SELECT OrderedDishes.dish_id 
        FROM CustomersOrders JOIN OrderedDishes ON(CustomersOrders.order_id = OrderedDishes.order_id)
        WHERE CustomersOrders.cust_id IS NULL
        GROUP BY OrderedDishes.dish_id 
        ORDER BY SUM(OrderedDishes.dish_amount) DESC, OrderedDishes.dish_id ASC
        LIMIT 1
    )
                                               
    '''
    query = sql.SQL(GET_MOST_PURCHASED_DISH_AMONG_ANONYMOUS_QUERY_FORMAT)
    _, rows_amount, data,_ = handle_query(query)
    if rows_amount > 1:
        assert (0)
    if data is None:
        return BadDish()
    return Dish(data[0]['dish_id'], data[0]['name'], data[0]['price'], data[0]['is_active'])


def did_customer_order_top_rated_dishes(cust_id: int) -> bool:
    DID_CUSTOMER_ORDER_TOP_RATED_DISHES_QUERY_FORMAT = '''

    SELECT DISTINCT  CustomersOrders.cust_id
    FROM CustomersOrders JOIN OrderedDishes ON(CustomersOrders.order_id = OrderedDishes.order_id)
    WHERE CustomersOrders.cust_id IS NOT NULL
                 AND CustomersOrders.cust_id = {cust_id}
                    AND OrderedDishes.dish_id IN(
                                            SELECT dish_id 
                                            FROM RatingScore
                                            ORDER BY avg_rating DESC , dish_id ASC
                                            LIMIT 5)
                                       
                           
    '''
    query = sql.SQL(DID_CUSTOMER_ORDER_TOP_RATED_DISHES_QUERY_FORMAT).format(
        cust_id=sql.Literal(cust_id)
    )
    _, rows_amount, _, _ = handle_query(query)
    return rows_amount > 0

# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API

def testSolutionQuery():
    GET_MIN_DISH = '''
        SELECT dish_id
        FROM RatingScore
        WHERE avg_rating < 3
        ORDER BY avg_rating ASC, dish_id ASC
        LIMIT 5
    '''

def get_customers_rated_but_not_ordered() -> List[int]:
    GET_MIN_RATED_DISHES = '''
        SELECT dish_id
            FROM RatingScore
            ORDER BY avg_rating ASC, dish_id ASC
            LIMIT 5
    '''
    GET_CUSTOMER_RATED_BUT_NOT_ORDER_QUERY_FORMAT = f'''
        SELECT DISTINCT(cust_low_ratings.cust_id) AS cust_id FROM 
        (
            SELECT cust_id, dish_id FROM DishRatings 
            WHERE rating < 3
        ) cust_low_ratings
        WHERE cust_low_ratings.dish_id IN ({GET_MIN_RATED_DISHES}) 
        AND cust_low_ratings.dish_id NOT IN 
        (
            SELECT cd.dish_id FROM CustomerOrderedDishes cd 
            WHERE cd.cust_id = cust_low_ratings.cust_id
        ) ORDER BY cust_id ASC;
    '''
    query = sql.SQL(GET_CUSTOMER_RATED_BUT_NOT_ORDER_QUERY_FORMAT)
    _, _, data, _ = handle_query(query)
    if data is None:
        return []
    return [row['cust_id'] for row in data]


def get_non_worth_price_increase() -> List[int]:
    GET_NON_WORTH_PRICE_INCREASE_QUERY_FORMAT = '''
        
        SELECT current.dish_id
        FROM Appo ap  JOIN 
                           (
                           SELECT Dish.dish_id AS dish_id ,Dish.price AS dish_price ,Appo.val AS val
                           FROM Appo JOIN Dish ON (Dish.dish_id = Appo.dish_id AND Dish.price= Appo.dish_price )
                           WHERE Dish.is_active=true
                           )AS current
                    ON(ap.dish_id = current.dish_id)
        WHERE current.dish_price - ap.dish_price >0 AND current.val - ap.val < 0
        ORDER BY current.dish_id ASC
    '''

    query = sql.SQL(GET_NON_WORTH_PRICE_INCREASE_QUERY_FORMAT)
    _, _, data, _ = handle_query(query)
    if data is None:
        return []
    return [row['dish_id'] for row in data]


def get_cumulative_profit_per_month(year: int) -> List[Tuple[int, float]]:
    GET_CUMULACTIVE_PROFILE_PER_MONTH_QUERY_FORMAT = '''
        SELECT COALESCE(SUM(total),0) AS val, coordinate.j AS month
        FROM 
            (SELECT *FROM (SELECT 1 AS i UNION ALL  SELECT 2 UNION ALL SELECT 3 
                UNION ALL SELECT 4 UNION ALL SELECT 5
                UNION ALL SELECT 6 UNION ALL SELECT 7 
                UNION ALL SELECT 8 UNION ALL SELECT 9
                UNION ALL SELECT 10 UNION ALL SELECT 11
                UNION ALL SELECT 12)   ,(SELECT 1 AS j UNION ALL  SELECT 2 UNION ALL SELECT 3 
                UNION ALL SELECT 4 UNION ALL SELECT 5
                UNION ALL SELECT 6 UNION ALL SELECT 7 
                UNION ALL SELECT 8 UNION ALL SELECT 9
                UNION ALL SELECT 10 UNION ALL SELECT 11
                UNION ALL SELECT 12)
                WHERE i <=j
                ) AS coordinate LEFT JOIN (
                    (SELECT     Orders.order_id AS order_id,
                                OrdersSum.total + OrdersSum.delivery_fee AS total,
                                EXTRACT(MONTH  FROM  Orders.date) AS month
                    FROM Orders JOIN OrdersSum ON (Orders.order_id = OrdersSum.order_id)
                    WHERE EXTRACT(YEAR FROM  Orders.date) = {year} ) 
                )ON(coordinate.i = month)
                group by coordinate.j
                ORDER BY  coordinate.j DESC
    '''
    query = sql.SQL(GET_CUMULACTIVE_PROFILE_PER_MONTH_QUERY_FORMAT).format(
        year=sql.Literal(year)
    )
    _, _, data, _ = handle_query(query)
    if data is None:
        return []  
    return [(row['month'], float(row['val'])) for row in data]


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    SELECTION_QUERY = f'''
    SELECT * FROM
    (
        (SELECT dish_id FROM
        (
            (SELECT b FROM
                (WITH RECURSIVE a_similar_b AS (
                    SELECT * FROM SimilarRelation
                    UNION 
                    SELECT a_to_b.a, b_to_c.b
                    FROM a_similar_b a_to_b JOIN SimilarRelation b_to_c ON a_to_b.b = b_to_c.a
                ) SELECT * FROM a_similar_b where a != b)
            WHERE a = {cust_id})
        ) rs JOIN DishRatings dr ON dr.cust_id = rs.b
        WHERE dr.rating >= 4)
        EXCEPT (SELECT dish_id FROM CustomerOrderedDishes WHERE cust_id = {cust_id})
    ) ORDER BY dish_id ASC;
    '''
    query = sql.SQL(SELECTION_QUERY)
    _, _, data, _ = handle_query(query)
    if data is None:
        return []
    return [row['dish_id'] for row in data]
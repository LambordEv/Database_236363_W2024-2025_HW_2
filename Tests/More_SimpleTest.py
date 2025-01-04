import unittest
from datetime import datetime

import Solution as Solution
from Business.Dish import Dish, BadDish
from Business.Order import Order, BadOrder
from Business.OrderDish import OrderDish
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''


class Test(AbstractTest):
    def test_customer(self) -> None:
        c1 = Customer(1, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 1.1')
        c2 = Customer(2, None, 21, "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'test 1.2') # full_name is NULL
        c3 = Customer(3, 'Yalla', 21, "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c3), 'test 1.3') # len(phone) != 10
        c4 = Customer(4, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 1.4')
        c5 = Customer(5, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c5), 'test 1.5')
        c6 = Customer(6, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c6), 'test 1.6')
        self.assertEqual(Customer(4, 'name', 21, "0123456789"),
                         Solution.get_customer(4), 'test 1.7')
        self.assertEqual(Customer(5, 'name', 21, "0123456789"),
                         Solution.get_customer(5), 'test 1.8')
        self.assertEqual(Customer(6, 'name', 21, "0123456789"),
                         Solution.get_customer(6), 'test 1.9')
        self.assertEqual(Customer(1, 'name', 21, "0123456789"),
                         Solution.get_customer(1), 'test 1.10')
        Solution.delete_customer(4)
        self.assertEqual(BadCustomer(), Solution.get_customer(4), 'test 1.11')
        Solution.delete_customer(5)
        self.assertEqual(BadCustomer(), Solution.get_customer(5), 'test 1.12')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_customer(c1), 'test 1.13')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_customer(30), 'test 1.14')
        c7 = Customer(-1, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c7), 'test 1.15') # cust_id < 0
        c8 = Customer(8, 'name', 2, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c8), 'test 1.16') # age < 18
        c9 = Customer(9, 'name', 2221, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c9), 'test 1.17') # age > 120
        c10 = Customer(None, 'name', 2221, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c10), 'test 1.18') # cust_id is NULL
        c11 = Customer(11, 'name', None, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c11), 'test 1.19') # age is NULL
        c12 = Customer(12, 'name', 21, None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c12), 'test 1.20') # phone is NULL


    def test_order(self) -> None:
        o1 = Order(1, datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   21, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 2.1')
        o2 = Order(1, datetime(year=3400, month=12, day=31, hour=23, minute=1, second=23),
                   21, "address 1")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_order(o2), 'test 2.2')
        o3 = Order(3, datetime(year=2055, month=12, day=31, hour=23, minute=1, second=23),
                   11, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 2.3')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(777), 'test 2.4')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_order(o1), 'test 2.5')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(3), 'test 2.6')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(3), 'test 2.7')
        self.assertEqual(Order(1, datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                               21, "address 1"), Solution.get_order(1), 'test 2.8')
        o4 = Order(4, datetime(year=1896, month=12, day=31, hour=23, minute=1, second=23),
                   11, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 3.1')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(4), 'test 3.2')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(4), 'test 3.3')
        o5 = Order(None, datetime(year=1990, month=12, day=31, hour=23, minute=1, second=23),
                   11, "address 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o5), 'test 3.4') # order_id is NULL
        o6 = Order(order_id=-333, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="barber 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o6), 'test 3.5') # order_id < 0
        o7 = Order(order_id=7, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=-333, delivery_address="blabla 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o7), 'test 3.6') # delivery_fee < 0
        o8 = Order(order_id=8, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=0, delivery_address=None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o8), 'test 3.7') # delivery_address is NULL
        o9 = Order(order_id=9, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=None, delivery_address="blabla 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o9), 'test 3.8') # delivery_fee is NULL
        self.assertEqual(BadOrder(), Solution.get_order(99999), 'test 3.9')
        o10 = Order(order_id=10, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                    delivery_fee=77, delivery_address="1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o10), 'test 3.9') # len(deliver_address) < 5
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 3.10')
        self.assertEqual(Order(4, datetime(year=1896, month=12, day=31, hour=23, minute=1, second=23),
                               11, "address 1"), Solution.get_order(4), 'test 3.11')

    def test_dish(self) -> None:
        d1 = Dish(dish_id=None, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d1), 'test 4.1') # dish_id is NULL
        d2 = Dish(dish_id=2, name=None, price=1, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d2), 'test 4.2') # name is NULL
        d3 = Dish(dish_id=3, name='100000', price=None, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d3), 'test 4.3') # price is NULL
        d4 = Dish(dish_id=4, name='1000000', price=3, is_active=None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d4), 'test 4.4') # is_active is NULL
        d5 = Dish(dish_id=-66666, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d5), 'test 4.5') # dish_id < 0
        d6 = Dish(dish_id=15, name='100000', price=-777777777, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d6), 'test 4.6') # price < 0
        d7 = Dish(dish_id=7, name='100000', price=0, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d7), 'test 4.7') # price == 0
        d8 = Dish(dish_id=8, name='1', price=8, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d8), 'test 4.8') # len(name) < 4
        d9 = Dish(dish_id=9, name='1111', price=9, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d9), 'test 4.9')
        d10 = Dish(dish_id=10, name='1111111', price=10, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d10), 'test 4.10')
        self.assertEqual(d9, Solution.get_dish(9), 'test 4.11')
        self.assertEqual(d10, Solution.get_dish(10), 'test 4.12')
        self.assertEqual(BadDish(), Solution.get_dish(99999), 'test 4.13')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(10, 50), 'test 4.14')
        _d10 = Dish(dish_id=10, name='1111111', price=50, is_active=True)
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.15')
        d11 = Dish(dish_id=11, name='1111111', price=10, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d11), 'test 4.16')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.update_dish_price(11, 30), 'test 4.17') # is_active = False
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.update_dish_price(10, -1), 'test 4.18') # price < 0
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(10, False), 'test 4.19')
        _d10.set_is_active(False)
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.20')
        _d10.set_is_active(True)
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(10, True), 'test 4.21')
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.22')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.update_dish_active_status(434343, True),'test 4.23')


    def test_clear_tables(self) -> None:
        c = Customer(10, 'name', 22, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c), 'test 5.1')
        o = Order(10, datetime(year=2055, month=12, day=31, hour=23, minute=1, second=23),
                  11, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o), 'test 5.2')
        d = Dish(dish_id=10, name='1111111', price=10, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d), 'test 5.3')
        self.assertEqual(c, Solution.get_customer(10), 'test 5.4')
        self.assertEqual(o, Solution.get_order(10), 'test 5.5')
        self.assertEqual(d, Solution.get_dish(10), 'test 5.6')
        Solution.clear_tables()
        self.assertEqual(BadCustomer(), Solution.get_customer(10), 'test 5.7')
        self.assertEqual(BadOrder(), Solution.get_order(10), 'test 5.8')
        self.assertEqual(BadDish(), Solution.get_dish(10), 'test 5.9')


    def test_customer_order(self) -> None:
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 6.1')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 6.2')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 6.3')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 6.4')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 6.5')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 6.6')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 6.7')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 6.8')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_placed_order(1, 1), 'test 6.9')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_placed_order(2, 1), 'test 6.10')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_placed_order(5, 5), 'test 6.11')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_placed_order(5, 2), 'test 6.12')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_placed_order(2, 5), 'test 6.13')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 2), 'test 6.14')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), 'test 6.15')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 6.16')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 4), 'test 6.17')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_placed_order(2, 4), 'test 6.18')
        ###################################
        ### get_customer_that_placed_order:
        ###################################
        self.assertEqual(Customer(cust_id=2, full_name='2', age=22, phone="0123456789"),
                         Solution.get_customer_that_placed_order(2), 'test 6.19')
        self.assertEqual(Customer(cust_id=3, full_name='3', age=22, phone="0123456789"),
                         Solution.get_customer_that_placed_order(3), 'test 6.20')
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(898989), 'test 6.21')

    def test_order_contains_dish(self) -> None:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 7.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 7.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 7.3')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 7.4')
        d2 = Dish(dish_id=2, name='yummy', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 7.5')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 7.6')
        d4 = Dish(dish_id=4, name='1000000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 7.7')
        d5 = Dish(dish_id=5, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 7.8')
        d6 = Dish(dish_id=6, name='100000', price=77, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 7.9')
        d7 = Dish(dish_id=7, name='100000', price=11, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 7.10')
        c1 = Customer(cust_id=1, full_name="Yossi", age=20, phone="0521234567")
        c2 = Customer(cust_id=2, full_name="Manyak", age=20, phone="0521234567")
        c3 = Customer(cust_id=3, full_name="Gid", age=20, phone="0521234567")
        c4 = Customer(cust_id=4, full_name="Vanyuchii", age=20, phone="0521234567")
        Solution.add_customer(c1)
        Solution.add_customer(c2)
        Solution.add_customer(c3)
        Solution.add_customer(c4)

        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 1), "Placing Order 1 for cust 1")
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 2), "Placing Order 2 for cust 2")
        # self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), "Placing Order 4 for cust 3")

        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.11')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=2, amount=10), 'test 7.12')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=1, amount=30), 'test 7.13') # 1 * 30 = 30 (2: 30)
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=2, amount=101), 'test 7.14') # 1 * 101 = 101 (2: 131)
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.15')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=7, amount=3),'test 7.16')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=10, dish_id=2, amount=3), 'test 7.17')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=10, dish_id=7, amount=3), 'test 7.18')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=10, dish_id=1, amount=3), 'test 7.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=7, is_active=True), 'test 7.20')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=7, amount=10), 'test 7.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=3, dish_id=7, amount=10), 'test 7.22')
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.order_contains_dish(order_id=2, dish_id=4, amount=-333), 'test 7.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=5, amount=1), 'test 7.24')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=5, is_active=False), 'test 7.25')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=2, dish_id=5, amount=3), 'test 7.26')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=5, is_active=True), 'test 7.27')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=5, amount=3), 'test 7.28') # 7 * 3 = 21 (2: 152)
        self.assertEqual(173.0, Solution.get_order_total_price(order_id=2), 'Total Price 1st Test') # (2: 152) + 21
        self.assertEqual([2], Solution.get_customers_spent_max_avg_amount_money(), 'Customer Spent Max Avg Money 1st Test')
        self.assertEqual(Dish(dish_id=7, name='100000', price=11, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'Most Purchase Dish in Un-Placed Orders - 1st')


        Solution.testSelectionFunction()
        ################################
        ### order_does_not_contain_dish:
        ################################
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_does_not_contain_dish(order_id=1, dish_id=1), 'test 7.30')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=5), 'test 7.31')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_does_not_contain_dish(order_id=1, dish_id=222), 'test 7.32')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_does_not_contain_dish(order_id=2222, dish_id=1), 'test 7.33')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_does_not_contain_dish(order_id=2222, dish_id=222), 'test 7.34')

    def test_get_all_order_items(self) -> None:
        # setup: insert orders o1 - o4, dishes d1 - d7.
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 8.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 8.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 8.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 8.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 8.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 8.6')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 8.7')
        d4 = Dish(dish_id=4, name='1000000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 8.8')
        d5 = Dish(dish_id=5, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 8.9')
        d6 = Dish(dish_id=6, name='100000', price=77, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 8.10')
        d7 = Dish(dish_id=7, name='100000', price=11, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 8.11')
        # add dishes to orders - o1 = { (dish_id=1, amount=2, price=1), (dish_id=2, amount=1, price=2) }
        #                        o2 = { }
        #                        o3 = { (dish_id=1, amount=5, price=1), (dish_id=3, amount=1, price=1),
        #                               (dish_id=4, amount=3, price=3), (dish_id=5, amount=7, price=7) }
        #                        o4 = { }
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1,1,2), 'test 8.12')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 2, 1), 'test 8.13')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 5), 'test 8.14')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 3, 1), 'test 8.15')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 4, 3), 'test 8.16')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 5, 7), 'test 8.17')
        o1_items = [OrderDish(1, 2, 1), OrderDish(2, 1, 2)]
        o2_items = []
        o3_items = [OrderDish(1, 5, 1), OrderDish(3, 1, 1),
                    OrderDish(4, 3, 3), OrderDish(5, 7, 7)]
        o4_items = []
        self.assertEqual(o1_items, Solution.get_all_order_items(order_id=1), 'test 8.18')
        self.assertEqual(o2_items, Solution.get_all_order_items(order_id=2), 'test 8.19')
        self.assertEqual(o3_items, Solution.get_all_order_items(order_id=3), 'test 8.20')
        self.assertEqual(o4_items, Solution.get_all_order_items(order_id=4), 'test 8.21')
        # remove some dishes:
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(order_id=1, dish_id=2), 'test 8.22')
        o1_items = [OrderDish(1, 2, 1)]
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(order_id=3, dish_id=1), 'test 8.23')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(order_id=3, dish_id=5), 'test 8.24')
        o3_items = [OrderDish(3, 1, 1), OrderDish(4, 3, 3)]
        self.assertEqual(o1_items, Solution.get_all_order_items(order_id=1), 'test 8.25')
        self.assertEqual(o3_items, Solution.get_all_order_items(order_id=3), 'test 8.26')

    def test_customer_rated_dish(self) -> None:
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 9.1')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 9.2')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 9.3')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 9.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 9.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 9.6')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 9.7')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=1), 'test 9.8')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=2, dish_id=1, rating=2), 'test 9.9')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=3, dish_id=1, rating=3), 'test 9.10')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=1, dish_id=2, rating=1), 'test 9.11')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=2, dish_id=2, rating=2), 'test 9.12')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=3, dish_id=2, rating=3), 'test 9.13')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=4, dish_id=1, rating=4), 'test 9.14')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=4, dish_id=2, rating=5), 'test 9.15')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=4, dish_id=3, rating=2), 'test 9.16')
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3, rating=111), 'test 9.17')
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3, rating=0), 'test 9.18')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3333, rating=4), 'test 9.19')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_rated_dish(cust_id=123123, dish_id=3, rating=4), 'test 9.20')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=1), 'test 9.21')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=3), 'test 9.22')
        ####################################
        ### customer_deleted_rating_on_dish:
        ####################################
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=5), 'test 9.24')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.25')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.26')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1111, dish_id=1), 'test 9.27')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1111), 'test 9.28')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1111, dish_id=1111), 'test 9.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=2), 'test 9.30')
        #############################
        ### get_all_customer_ratings:
        #############################
        # current rating are:
        c1_ratings = [(1, 2), (2, 1)]
        c2_ratings = [(1, 2), (2, 2)]
        c3_ratings = [(1, 3), (2, 3)]
        c4_ratings = [(1, 4), (2, 5), (3, 2)]
        self.assertEqual(c1_ratings, Solution.get_all_customer_ratings(1), 'test 9.31')
        self.assertEqual(c2_ratings, Solution.get_all_customer_ratings(2), 'test 9.32')
        self.assertEqual(c3_ratings, Solution.get_all_customer_ratings(3), 'test 9.33')
        self.assertEqual(c4_ratings, Solution.get_all_customer_ratings(4), 'test 9.34')
        # delete c1's ratings:
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.35')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=2), 'test 9.36')
        self.assertEqual([], Solution.get_all_customer_ratings(1), 'test 9.37')
        # mix-up order of ratings to check ORDER BY dish_id:
        d4 = Dish(dish_id=4, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 9.38')
        d5 = Dish(dish_id=5, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 9.39')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=5, rating=1), 'test 9.40')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=2, rating=4), 'test 9.41')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3, rating=2), 'test 9.42')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=2), 'test 9.43')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=4, rating=5), 'test 9.44')
        c1_ratings = [(1, 2), (2, 4), (3, 2), (4, 5), (5, 1)]
        self.assertEqual(c1_ratings, Solution.get_all_customer_ratings(1), 'test 9.45')



# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)

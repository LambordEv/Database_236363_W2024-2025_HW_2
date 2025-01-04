import unittest
from datetime import datetime

import Solution as Solution
from Solution import *
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
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.update_dish_price(10, -1), 'test 4.18') # price < 0
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(10, False), 'test 4.19')
        _d10.set_is_active(False)
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.20')
        _d10.set_is_active(True)
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(10, True), 'test 4.21')
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.22')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_active_status(434343, True), 'test 4.23')



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
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.11')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=2, amount=10), 'test 7.12')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=1, amount=30), 'test 7.13')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=2, amount=101), 'test 7.14')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.15')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_contains_dish(order_id = 1, dish_id = 7, amount = 3), 'test 7.16')
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
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.order_contains_dish(order_id=2, dish_id=4, amount=-333), 'test 7.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=5, amount=10), 'test 7.24')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=5, is_active=False), 'test 7.25')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=2, dish_id=5, amount=3), 'test 7.26')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=5, is_active=True), 'test 7.27')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=5, amount=3), 'test 7.28')
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
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 1, 2), 'test 8.12')
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



    def test_get_order_total_price(self) -> None:
        return
        ##### initial setup ############################################################################
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 10.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 10.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 10.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 10.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 10.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 10.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 10.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 10.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 10.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 10.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 10.11')
        ################################################################################################
        # order total prices include only delivery_fee:
        self.assertEqual(1, Solution.get_order_total_price(1), 'test 10.12')
        self.assertEqual(2, Solution.get_order_total_price(2), 'test 10.13')
        self.assertEqual(3, Solution.get_order_total_price(3), 'test 10.14')
        # add dishes to orders:
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,1), 'test 10.15')
        self.assertEqual(1 + 1, Solution.get_order_total_price(1), 'test 10.16')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 2, 2), 'test 10.16')
        self.assertEqual(1 + 1 + (2 * 2), Solution.get_order_total_price(1), 'test 10.17')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 1, 1), 'test 10.18')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 1), 'test 10.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 3, 1), 'test 10.20')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 4, 1), 'test 10.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 5, 1), 'test 10.22')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 6, 1), 'test 10.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 7, 1), 'test 10.24')
        self.assertEqual(2 + 1 + 2 + 3 + 4 + 5 + 6 + 7, Solution.get_order_total_price(2), 'test 10.25')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(2, 3), 'test 10.26')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(2, 6), 'test 10.27')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(2, 1), 'test 10.28')
        self.assertEqual(2 + 2 + 4 + 5 + 7, Solution.get_order_total_price(2), 'test 10.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 777), 'test 10.30')
        self.assertEqual(3 + 777, Solution.get_order_total_price(3), 'test 10.31')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(3, 1), 'test 10.32')
        self.assertEqual(3, Solution.get_order_total_price(3), 'test 10.33')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 444), 'test 10.34')
        self.assertEqual(3 + 444, Solution.get_order_total_price(3), 'test 10.35')



    def test_get_customers_spent_max_avg_amount_money(self) -> None:
        return
        ##### initial setup ############################################################################
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 11.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 11.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 11.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 11.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 11.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 11.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 11.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 11.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 11.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 11.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 11.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 11.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 11.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 11.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 11.15')
        ################################################################################################
        max_spenders = []
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.16')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 11.17')
        max_spenders = [1]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.18')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 1, 4), 'test 11.19')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(2, 2, 1), 'test 11.20')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 2), 'test 11.21')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(3, 3, 1), 'test 11.22')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 3), 'test 11.23')
        max_spenders = [2] # c1 spent (delivery = )1 + (price*amount = )4 on o1,
        # (delivery = )2 + (price*amount = )2 on o2,
        # so (5 + 4) / 2 = 4.5, while c2 spent (delivery)3 + (price*amount)3 on o3
        # so c1's avg spending is 4.5 < c2's avg spending = 6
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.24')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 4), 'test 11.25')
        # now c1 spent even less on average (total of o4 is only delivery_fee, which is 4)
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.26')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 1, 5), 'test 11.27')
        # now c1 spent total(o1) + total(o2) + total(o4) = 5 + 4 + 9
        # and so average_spending(c1) = 18 / 3 = 6 = average_spending(c2)
        max_spenders = [1, 2]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.28')
        o44 = Order(order_id=44, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address") # notice that delivery_fee == 4, not 44
        self.assertEqual(ReturnValue.OK, Solution.add_order(o44), 'test 11.29')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 44), 'test 11.30')
        # no change in max_spenders
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.31')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(44, 1, 2), 'test 11.32')
        # add c3 to max_spenders
        max_spenders = [1, 2, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.33')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(44, 2, 1), 'test 11.34')
        # c3 placed order o4
        max_spenders = [3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.35')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(3), 'test 11.36')
        max_spenders = [1, 2]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(),'test 11.37')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 11.38')
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.39')
        o5 = Order(order_id=5, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=5, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o5), 'test 11.40')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(5, 1, 1), 'test 11.41')
        # total(o5) = 5 + 1 = 6
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 5), 'test 11.42')
        max_spenders = [1, 2, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.43')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(2), 'test 11.44')
        max_spenders = [1, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.45')
        o11 = Order(order_id=11, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address") # note that delivery_fee of o11 is 1, not 11
        self.assertEqual(ReturnValue.OK, Solution.add_order(o11), 'test 11.46')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_placed_order(1, 11), 'test 11.47')
        # now average_spending(c1) < average_spending(c3)
        max_spenders = [3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.48')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(11, 1, 5), 'test 11.49')
        # and again average_spending(c1) = average_spending(c3) = 6
        max_spenders = [1, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.50')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #

    def test_get_most_purchased_dish_among_anonymous_order(self) -> None:
        return
        ##### initial setup ############################################################################
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 12.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 12.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 12.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 12.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 12.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 12.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 12.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 12.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 12.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 12.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 12.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 12.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 12.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 12.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 12.15')
        ################################################################################################
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 2), 'test 12.16')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.17')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 1, 1), 'test 12.18')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 2, 1), 'test 12.20')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 2), 'test 12.22')
        self.assertEqual(Dish(dish_id=1, name='10000', price=1, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.23')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 12.24')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.25')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(1), 'test 12.26')
        # o1 does not belong to c1 anymore
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 12.27')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 3, 1), 'test 12.28')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 3, 1), 'test 12.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 3, 1), 'test 12.30')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 3, 1), 'test 12.31')
        self.assertEqual(Dish(dish_id=3, name='100000', price=3, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.32')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), 'test 12.33')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(4,4,1), 'test 12.34')
        # @TODO: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # @TODO: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # @TODO: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # @TODO: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.assertEqual(Dish(dish_id=3, name='100000', price=3, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.35') # FIXED
        self.assertEqual(ReturnValue.OK, Solution.delete_order(1), 'test 12.36')
        o2_dishes = [OrderDish(2, 2, 2), OrderDish(3, 1, 3)]
        o3_dishes = [OrderDish(1, 2, 1), OrderDish(2, 1, 2),
                    OrderDish(3, 1, 3)]
        o4_dishes = [OrderDish(3, 1, 3), OrderDish(4, 1, 4)]
        self.assertEqual(o2_dishes, Solution.get_all_order_items(2),'test 12.37')
        self.assertEqual(o3_dishes, Solution.get_all_order_items(3), 'test 12.38')
        self.assertEqual(o4_dishes, Solution.get_all_order_items(4), 'test 12.39')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.40') # FIXED
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(3, 3), 'test 12.41')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.42') # FIXED
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(3, 2), 'test 12.43')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.44')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(4, 2), 'test 12.45')
        self.assertEqual(Dish(dish_id=3, name='100000', price=3, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.46')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #

    def test_did_customer_order_top_rated_dishes(self) -> None:
        return
        ##### initial setup ############################################################################
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 13.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 13.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 13.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 13.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 13.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 13.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 13.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 13.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 13.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 13.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 13.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 13.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 13.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 13.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 13.15')
        ################################################################################################
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(1), 'test 13.16')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(2), 'test 13.17')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.18')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4),'test 13.19')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,1), 'test 13.20')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2,1,1), 'test 13.21')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 13.22')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 2), 'test 13.23')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 2), 'test 13.24')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(1), 'test 13.25')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.26')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.27')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4),'test 13.28')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 1, 3), 'test 13.29')
        # d1's average rating = (1 + 3) / 2 = 2
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(1), 'test 13.30')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.31')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.32')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.33')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 1, 5), 'test 13.34')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(4, 1, 5), 'test 13.35')
        # d1's average rating = (1 + 3 + 5 + 5) / 4 = 3.5
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.36')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.37')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.38')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.39')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 2, 5), 'test 13.40')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2, 2, 5), 'test 13.41')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 2, 5), 'test 13.42')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(4, 2, 5), 'test 13.43')
        # d1's average rating = (1 + 3 + 5 + 5) / 4 = 3.5
        # d2's average rating = 5*4 / 4 = 5
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 2, 2), 'test 13.44')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), 'test 13.45')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.46')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.47')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(3), 'test 13.48')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.49')
        c5 = Customer(cust_id=5, full_name='5', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c5), 'test 13.50')
        c6 = Customer(cust_id=6, full_name='6', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c6), 'test 13.51')
        c7 = Customer(cust_id=7, full_name='7', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c7), 'test 13.52')
        c8 = Customer(cust_id=8, full_name='8', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c8), 'test 13.53')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(5, 2, 1), 'test 13.54')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(6, 2, 1), 'test 13.55')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(7, 2, 1), 'test 13.56')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(8, 2, 1), 'test 13.57')
        # d2's average rating = (5*4 + 1*4) / 8 = 3
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.58')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.59')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(3), 'test 13.60')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.61')
        c9 = Customer(cust_id=9, full_name='9', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c9), 'test 13.62')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(9, 2, 1), 'test 13.63')
        # d2's average rating = (5*4 + 1*5) / 9 = 2.777777778
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.64')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(2), 'test 13.65')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.66')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.67')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(4, 4), 'test 13.68')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.69')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 2, 2), 'test 13.70')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.71')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 7, 1), 'test 13.72')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.73')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 6, 1), 'test 13.74')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.75')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(9, 6, 1), 'test 13.76')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.77')
        c10 = Customer(cust_id=10, full_name='10', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c10), 'test 13.78')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(10, 2, 5), 'test 13.79')
        # d2's average rating = (5*4 + 1*5 + 5) / 10 =3
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.80')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(10, 2), 'test 13.81')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.82')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(4, 7), 'test 13.83')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.84')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #

    def test_get_customers_rated_but_not_ordered(self) -> None:
        return
        ##### initial setup ############################################################################
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 14.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 14.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 14.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 14.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 14.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 14.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 14.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 14.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 14.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 14.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 14.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 14.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 14.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 14.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 14.15')
        ################################################################################################
        customers_rated_not_ordered = []
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.16')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(4,1,1), 'test 14.17')
        customers_rated_not_ordered = [4]
        Solution.testSelectionFunction()
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.18')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 1, 1), 'test 14.19')
        customers_rated_not_ordered = [1, 4]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.20')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 1, 1), 'test 14.21')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 14.22')
        customers_rated_not_ordered = [4]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.23')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(1), 'test 14.24')
        customers_rated_not_ordered = [1, 4]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.25')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 14.26')
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.27')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 1, 1), 'test 14.28')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2, 1, 1), 'test 14.29')
        customers_rated_not_ordered = [1, 2, 3, 4]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.30')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(2), 'test 14.31')
        customers_rated_not_ordered = [1, 3, 4]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.32')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(3), 'test 14.33')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(1), 'test 14.34')
        customers_rated_not_ordered = [4]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.35')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 14.36')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 14.37')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 14.38')
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.39')
        self.assertEqual(ReturnValue.OK, Solution.customer_deleted_rating_on_dish(4,1), 'test 14.40')
        customers_rated_not_ordered = []
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.41')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 1, 1), 'test 14.42')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 2, 1), 'test 14.43')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 3, 1), 'test 14.44')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2, 1, 3), 'test 14.45')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 1, 3), 'test 14.46')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(4, 1, 4), 'test 14.46')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(1), 'test 14.47')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(2), 'test 14.48')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(3), 'test 14.49')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(4), 'test 14.50')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 14.51')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 14.52')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 14.53')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 14.54')
        customers_rated_not_ordered = [1]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.55')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 1, 1), 'test 14.56')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 1), 'test 14.57')
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.58')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 2, 8), 'test 14.59')
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.60')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 3, 7), 'test 14.61')
        customers_rated_not_ordered = []
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.62')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 7, 2), 'test 14.63')
        customers_rated_not_ordered = [1]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.64')
        Solution.clear_tables()
        ##### again - initial setup ############################################################################
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23), delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 14.65')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23), delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 14.66')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23), delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 14.67')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23), delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 14.68')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 14.69')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 14.70')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 14.71')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 14.72')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 14.73')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 14.74')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 14.75')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 14.76')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 14.77')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 14.78')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 14.79')
        ################################################################################################
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 7, 5), 'test 14.80')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2, 7, 1), 'test 14.81')
        customers_rated_not_ordered = []
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.82')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 6, 5), 'test 14.83')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2, 6, 1), 'test 14.84')
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.85')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 7, 1), 'test 14.86')
        customers_rated_not_ordered = [2, 3]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.87')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(4, 7, 777), 'test 14.88')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 4), 'test 14.89')
        customers_rated_not_ordered = [3]
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.90')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(4, 6, 111), 'test 14.91')
        self.assertEqual(customers_rated_not_ordered, Solution.get_customers_rated_but_not_ordered(), 'test 14.92')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #

    def test_get_non_worth_price_increase(self) -> None:
        return
        self.assertEqual([], Solution.get_non_worth_price_increase(), 'test 15.1')
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 15.2')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 15.3')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 15.4')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,8), 'test 15.5')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1,4), 'test 15.6')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 1, 1), 'test 15.7')
        dishes_non_worth_increase = [1]
        self.assertEqual(dishes_non_worth_increase, Solution.get_non_worth_price_increase(), 'test 15.8')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1, 1), 'test 15.9')
        dishes_non_worth_increase = []
        self.assertEqual(dishes_non_worth_increase, Solution.get_non_worth_price_increase(), 'test 15.10')

        clear_tables()
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 15.11')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 15.12')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 15.13')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 15.14')
        o5 = Order(order_id=5, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o5), 'test 15.15')
        o6 = Order(order_id=6, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o6), 'test 15.16')
        o7 = Order(order_id=7, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o7), 'test 15.17')
        o8 = Order(order_id=8, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o8), 'test 15.18')

        # notice that all dish prices are initially 1
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 15.19')
        d2 = Dish(dish_id=2, name='yummy', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 15.20')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 15.21')
        d4 = Dish(dish_id=4, name='1000000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 15.22')
        d5 = Dish(dish_id=5, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 15.23')
        d6 = Dish(dish_id=6, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 15.24')
        d7 = Dish(dish_id=7, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 15.25')

        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 15.26')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 15.27')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 15.28')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 15.29')

        dishes_non_worth_increase = []
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.30')
        order_contains_dish(1, 1, 10)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.31')
        update_dish_price(1,5)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.32')
        order_contains_dish(2, 1, 1)
        dishes_non_worth_increase = [1]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.33')
        update_dish_active_status(1, False)
        dishes_non_worth_increase = []
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.34')
        order_contains_dish(1, 2, 1)
        order_contains_dish(2, 2, 1)
        order_contains_dish(3, 2, 1)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.35')
        update_dish_active_status(2, False)
        update_dish_price(2, 10)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.36')
        update_dish_active_status(2, True)
        update_dish_active_status(1, True)
        dishes_non_worth_increase = [1]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.37')
        order_contains_dish(4, 2, 1)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.38')
        order_contains_dish(5, 2, 2)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.39')
        update_dish_price(2, 15)
        order_contains_dish(6, 2, 2)
        dishes_non_worth_increase = [1]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.40')
        order_contains_dish(7, 2, 2)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.41')
        update_dish_price(2, 20)
        order_contains_dish(8, 2, 1)
        dishes_non_worth_increase = [1, 2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.42')
        update_dish_active_status(1, False)
        dishes_non_worth_increase = [2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.43')
        update_dish_active_status(1, True)
        dishes_non_worth_increase = [1, 2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.44')
        update_dish_price(1, 100)
        dishes_non_worth_increase = [2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.45')
        order_contains_dish(3, 1, 2)
        order_contains_dish(4, 1, 1)
        update_dish_price(1, 120)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.46')
        order_contains_dish(5, 1, 1)
        dishes_non_worth_increase = [1, 2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.47')
        order_contains_dish(1, 3, 3)
        order_contains_dish(2, 3, 3)
        order_contains_dish(3, 3, 3)
        order_contains_dish(4, 3, 3)
        order_contains_dish(5, 3, 3)
        order_contains_dish(6, 3, 3)
        order_contains_dish(1, 4, 4)
        order_contains_dish(2, 4, 4)
        order_contains_dish(3, 4 ,4)
        order_contains_dish(4, 4, 4)
        order_contains_dish(5, 4, 4)
        order_contains_dish(6, 4, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.48')
        update_dish_price(4, 2)
        order_contains_dish(7, 4, 1)
        dishes_non_worth_increase = [1, 2, 4]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.49')
        update_dish_price(4, 3)
        order_contains_dish(8, 4, 1)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.50')
        order_does_not_contain_dish(1, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.51')
        order_does_not_contain_dish(2, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.52')
        order_does_not_contain_dish(3, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.53')
        order_does_not_contain_dish(4, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.54')
        order_does_not_contain_dish(5, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.55')
        order_does_not_contain_dish(6, 4)
        dishes_non_worth_increase = [1, 2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.56')
        order_does_not_contain_dish(8, 4)
        order_contains_dish(1, 4, 2)
        update_dish_price(4, 5)
        order_contains_dish(2, 4, 1)
        dishes_non_worth_increase = [1, 2, 4]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.57')
        update_dish_active_status(4, False)
        dishes_non_worth_increase = [1, 2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.58')
        update_dish_active_status(4, True)
        dishes_non_worth_increase = [1, 2, 4]
        customer_placed_order(1, 1)
        customer_placed_order(1, 2)
        customer_placed_order(2, 3)
        customer_placed_order(3, 4)
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.59')
        update_dish_active_status(4, False)
        dishes_non_worth_increase = [1, 2]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.60')

        clear_tables()
        # test case from hw2.pdf:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 15.61')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 15.62')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 15.63')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 15.64')
        dishes_non_worth_increase = []
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.65')
        d1 = Dish(dish_id=1, name='10000', price=40, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 15.66')
        order_contains_dish(3, 1, 2)
        order_contains_dish(4, 1, 2)
        update_dish_price(1, 50)
        order_contains_dish(1, 1, 1)
        order_contains_dish(2, 1, 2)
        dishes_non_worth_increase = [1]
        self.assertEqual(dishes_non_worth_increase, get_non_worth_price_increase(), 'test 15.67')


    def test_get_cumulative_profit_per_month(self) -> None:
        return
        # year = 1000:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=29, hour=3, minute=1, second=11),
                   delivery_fee=1, delivery_address="addradsad")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 16.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=10, day=31, hour=2, minute=2, second=12),
                   delivery_fee=2, delivery_address="addrffaf")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 16.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=11, day=10, hour=23, minute=21, second=2),
                   delivery_fee=3, delivery_address="adsfdfass")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 16.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=7, day=30, hour=23, minute=12, second=0),
                   delivery_fee=4, delivery_address="adaaadess")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 16.4')
        o5 = Order(order_id=5, date=datetime(year=1000, month=7, day=11, hour=23, minute=14, second=1),
                   delivery_fee=5, delivery_address="hjklhjhgress")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o5), 'test 16.5')
        o6 = Order(order_id=6, date=datetime(year=1000, month=10, day=21, hour=23, minute=35, second=27),
                   delivery_fee=6, delivery_address="asdgsdg")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o6), 'test 16.6')
        o7 = Order(order_id=7, date=datetime(year=1000, month=2, day=15, hour=23, minute=38, second=23),
                   delivery_fee=7, delivery_address="addrafgas")

        # year = 1800
        self.assertEqual(ReturnValue.OK, Solution.add_order(o7), 'test 16.7')
        o8 = Order(order_id=8, date=datetime(year=1800, month=9, day=11, hour=23, minute=1, second=55),
                   delivery_fee=8, delivery_address="adasdasdess")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o8), 'test 16.8')
        o9 = Order(order_id=9, date=datetime(year=1800, month=9, day=3, hour=20, minute=11, second=27),
                   delivery_fee=9, delivery_address="addddddds")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o9), 'test 16.9')
        o10 = Order(order_id=10, date=datetime(year=1800, month=9, day=6, hour=14, minute=12, second=29),
                   delivery_fee=10, delivery_address="addrassddasess")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o10), 'test 16.10')
        o11 = Order(order_id=11, date=datetime(year=1800, month=5, day=4, hour=2, minute=19, second=23),
                   delivery_fee=11, delivery_address="addreaass")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o11), 'test 16.11')
        o12 = Order(order_id=12, date=datetime(year=1800, month=5, day=14, hour=23, minute=56, second=13),
                   delivery_fee=12, delivery_address="addressds")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o12), 'test 16.12')
        o13 = Order(order_id=13, date=datetime(year=1800, month=5, day=31, hour=7, minute=49, second=25),
                   delivery_fee=13, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o13), 'test 16.13')

        # year = 1950
        o14 = Order(order_id=14, date=datetime(year=1950, month=1, day=2, hour=3, minute=13, second=23),
                   delivery_fee=14, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o14), 'test 16.14')
        o15 = Order(order_id=15, date=datetime(year=1950, month=2, day=1, hour=23, minute=2, second=3),
                   delivery_fee=15, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o15), 'test 16.15')
        o16 = Order(order_id=16, date=datetime(year=1950, month=3, day=3, hour=23, minute=6, second=33),
                   delivery_fee=16, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o16), 'test 16.16')

        # year = 1300
        o17 = Order(order_id=17, date=datetime(year=1300, month=1, day=31, hour=9, minute=56, second=26),
                   delivery_fee=17, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o17), 'test 16.17')
        o18 = Order(order_id=18, date=datetime(year=1300, month=1, day=31, hour=8, minute=57, second=12),
                   delivery_fee=18, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o18), 'test 16.18')
        o19 = Order(order_id=19, date=datetime(year=1300, month=9, day=9, hour=7, minute=3, second=13),
                   delivery_fee=19, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o19), 'test 16.19')
        o20 = Order(order_id=20, date=datetime(year=1300, month=11, day=1, hour=14, minute=12, second=23),
                   delivery_fee=20, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o20), 'test 16.20')
        o21 = Order(order_id=21, date=datetime(year=1300, month=7, day=2, hour=15, minute=16, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o21), 'test 16.21')
        o22 = Order(order_id=22, date=datetime(year=1300, month=5, day=23, hour=11, minute=6, second=47),
                   delivery_fee=22, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o22), 'test 16.22')
        o23 = Order(order_id=23, date=datetime(year=1300, month=1, day=15, hour=3, minute=1, second=55),
                   delivery_fee=23, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o23), 'test 16.23')
        o24 = Order(order_id=24, date=datetime(year=1300, month=3, day=11, hour=2, minute=1, second=23),
                   delivery_fee=24, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o24), 'test 16.24')

        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 16.25')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 16.26')
        d3 = Dish(dish_id=3, name='daldasl', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 16.27')
        d4 = Dish(dish_id=4, name='ggggg', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 16.28')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 16.29')
        d6 = Dish(dish_id=6, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 16.30')
        d7 = Dish(dish_id=7, name='10sss00', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 16.31')
        d8 = Dish(dish_id=8, name='1xaxax', price=8, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d8), 'test 16.32')

        d9 = Dish(dish_id=9, name='10fff0', price=9, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d9), 'test 16.33')
        d10 = Dish(dish_id=10, name='yummy', price=10, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d10), 'test 16.34')
        d11 = Dish(dish_id=11, name='bklads', price=11, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d11), 'test 16.35')
        d12 = Dish(dish_id=12, name='1eee00', price=12, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d12), 'test 16.36')
        d13 = Dish(dish_id=13, name='100000', price=13, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d13), 'test 16.37')
        d14 = Dish(dish_id=14, name='100ytt0', price=14, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d14), 'test 16.38')
        d15 = Dish(dish_id=15, name='100aeg0', price=15, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d15), 'test 16.39')
        d16 = Dish(dish_id=16, name='10006', price=16, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d16), 'test 16.40')

        order_contains_dish(1,1,1)
        order_contains_dish(9,1,1)
        order_contains_dish(24,4,4)
        order_contains_dish(10,13,13)
        order_contains_dish(1,10,10)
        order_contains_dish(14,15,15)
        order_contains_dish(14,2,2)
        order_contains_dish(19,11,11)
        order_contains_dish(3,7,7)
        order_contains_dish(4,7,7)
        order_contains_dish(5,7,7)
        order_contains_dish(3,8,8)
        order_contains_dish(16,1,1)
        order_contains_dish(16,2,2)
        order_contains_dish(15,1,1)
        order_contains_dish(16,3,3)
        order_contains_dish(21,12,12)
        order_contains_dish(21,5,5)
        order_contains_dish(8,10,10)
        order_contains_dish(8,9,9)
        order_contains_dish(16,10,10)

        cumulative_profits_1000 = [
            (12, 340),
            (11, 238),
            (10, 122),
            (9, 114),
            (8, 114),
            (7, 114),
            (6, 7),
            (5, 7),
            (4, 7),
            (3, 7),
            (2, 7),
            (1, 0)
        ]
        cumulative_profits_1800 = [
            (12, 414),
            (11, 414),
            (10, 414),
            (9, 414),
            (8, 36),
            (7, 36),
            (6, 36),
            (5, 36),
            (4, 0),
            (3, 0),
            (2, 0),
            (1, 0)
        ]
        cumulative_profits_1950 = [
            (12, 389),
            (11, 389),
            (10, 389),
            (9, 389),
            (8, 389),
            (7, 389),
            (6, 389),
            (5, 389),
            (4, 389),
            (3, 389),
            (2, 259),
            (1, 243)
        ]
        cumulative_profits_1300 = [
            (12, 470),
            (11, 470),
            (10, 450),
            (9, 450),
            (8, 310),
            (7, 310),
            (6, 120),
            (5, 120),
            (4, 98),
            (3, 98),
            (2, 58),
            (1, 58)
        ]

        self.assertEqual(cumulative_profits_1000, get_cumulative_profit_per_month(1000), 'test 16.41')
        self.assertEqual(cumulative_profits_1800, get_cumulative_profit_per_month(1800), 'test 16.42')
        self.assertEqual(cumulative_profits_1950, get_cumulative_profit_per_month(1950), 'test 16.43')
        self.assertEqual(cumulative_profits_1300, get_cumulative_profit_per_month(1300), 'test 16.44')


    def test_get_potential_dish_recommendations(self) -> None:
        return
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 17.1')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 17.2')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 17.3')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 17.4')

        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 17.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 17.6')
        d3 = Dish(dish_id=3, name='daldasl', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 17.7')
        d4 = Dish(dish_id=4, name='ggggg', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 17.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 17.9')
        d6 = Dish(dish_id=6, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 17.10')
        d7 = Dish(dish_id=7, name='10sss00', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 17.11')

        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=29, hour=3, minute=1, second=11),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 17.12')

        # the test case provided in hw2.pdf:
        order_contains_dish(1,1,1)
        order_contains_dish(1,2,1)
        order_contains_dish(1,3,1)
        customer_placed_order(1,1)

        customer_rated_dish(1,1,4)
        customer_rated_dish(1,2,5)
        customer_rated_dish(1,3,4)

        customer_rated_dish(2,1,5)
        customer_rated_dish(2,4,4)

        customer_rated_dish(3,4,5)
        customer_rated_dish(3,5,5)
        customer_rated_dish(3,7,4)

        customer_rated_dish(4,6,5)

        c1_recommended_dishes = [4, 5, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.13')

        # and some more tests
        customer_rated_dish(4,5,3)
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.14')

        customer_deleted_rating_on_dish(4, 5)
        customer_rated_dish(4,5,4)
        c1_recommended_dishes = [4, 5, 6, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.15')

        customer_deleted_rating_on_dish(2, 4)
        c1_recommended_dishes = []
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.16')

        customer_rated_dish(3, 2, 5)
        c1_recommended_dishes = [4, 5, 6, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.17')

        order_contains_dish(1,5,111)
        c1_recommended_dishes = [4, 6, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.18')

        order_contains_dish(1, 4, 111)
        c1_recommended_dishes = [6, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.19')

        order_contains_dish(1, 7, 111)
        c1_recommended_dishes = [6]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.20')

        delete_order(1)
        add_order(o1)
        customer_placed_order(1,1)
        order_contains_dish(1,2,343)
        customer_deleted_rating_on_dish(1,1)
        customer_deleted_rating_on_dish(1,3)
        c1_recommended_dishes = [4, 5, 6, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.21')

        order_contains_dish(1,5,3333)
        customer_rated_dish(1,5,2)
        c1_recommended_dishes = [4, 6, 7]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.22')

        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=29, hour=3, minute=1, second=11),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 17.23')
        order_contains_dish(2,1,777)
        customer_placed_order(2,2)
        c2_recommended_dishes = []
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.24')

        customer_rated_dish(4,1,4)
        c2_recommended_dishes = [2, 4, 5, 6, 7]
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.25')

        order_contains_dish(1,3, 20)
        customer_rated_dish(1, 3, 4)

        c2_recommended_dishes = [2, 3, 4, 5, 6, 7]
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.26')

        customer_deleted_rating_on_dish(1,2)
        c2_recommended_dishes = [2, 4, 5, 6, 7]
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.27')

        customer_deleted_rating_on_dish(1, 5)
        order_contains_dish(1, 5, 4444444)
        customer_rated_dish(1,5,5)
        c2_recommended_dishes = [2, 3, 4, 5, 6, 7]
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.28')

        customer_deleted_rating_on_dish(3,5)
        c2_recommended_dishes = [3, 5, 6]
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.29')

        customer_deleted_rating_on_dish(1,5)
        c2_recommended_dishes = [5, 6]
        self.assertEqual(c2_recommended_dishes, get_potential_dish_recommendations(2), 'test 17.30')

        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=29, hour=3, minute=1, second=11),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 17.31')
        customer_placed_order(3,3)
        order_contains_dish(3,2,123)
        order_contains_dish(3,4,11231)
        order_contains_dish(3,7,12)
        c3_recommended_dishes = []
        self.assertEqual(c3_recommended_dishes, get_potential_dish_recommendations(3), 'test 17.32')

        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=29, hour=3, minute=1, second=11),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 17.33')
        customer_placed_order(4,4)
        order_contains_dish(4,1,12222)
        order_contains_dish(4,5,12222)
        order_contains_dish(4,6,1243)
        c4_recommended_dishes = []
        self.assertEqual(c4_recommended_dishes, get_potential_dish_recommendations(4), 'test 17.33')

        customer_rated_dish(2,2,5)
        c4_recommended_dishes = [2, 4, 7]
        self.assertEqual(c4_recommended_dishes, get_potential_dish_recommendations(4), 'test 17.34')

        customer_rated_dish(1,2,5)
        c4_recommended_dishes = [2, 3, 4, 7]
        self.assertEqual(c4_recommended_dishes, get_potential_dish_recommendations(4), 'test 17.35')

        clear_tables()
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1))
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2))
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3))
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4))
        c5 = Customer(cust_id=5, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c5))
        c6 = Customer(cust_id=6, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c6))
        c7 = Customer(cust_id=7, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c7))
        c8 = Customer(cust_id=8, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c8))
        c9 = Customer(cust_id=9, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c9))
        c10 = Customer(cust_id=10, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c10))
        c11 = Customer(cust_id=11, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c11))
        c12 = Customer(cust_id=12, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c12))
        c13 = Customer(cust_id=13, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c13))
        c14 = Customer(cust_id=14, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c14))
        c15 = Customer(cust_id=15, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c15))
        c16 = Customer(cust_id=16, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c16))

        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2))
        d3 = Dish(dish_id=3, name='daldasl', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3))
        d4 = Dish(dish_id=4, name='ggggg', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4))
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5))
        d6 = Dish(dish_id=6, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6))
        d7 = Dish(dish_id=7, name='10sss00', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7))
        d8 = Dish(dish_id=8, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d8))
        d9 = Dish(dish_id=9, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d9))
        d10 = Dish(dish_id=10, name='daldasl', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d10))
        d11 = Dish(dish_id=11, name='ggggg', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d11))
        d12 = Dish(dish_id=12, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d12))
        d13 = Dish(dish_id=13, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d13))
        d14 = Dish(dish_id=14, name='10sss00', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d14))
        d15 = Dish(dish_id=15, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d15))
        d16 = Dish(dish_id=16, name='10sss00', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d16))
        d17 = Dish(dish_id=17, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d17))
        d18 = Dish(dish_id=18, name='10sss00', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d18))
        d19 = Dish(dish_id=19, name='1afa0gg', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d19))


        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=29, hour=3, minute=1, second=11),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1))

        customer_placed_order(1,1)
        order_contains_dish(1,1,1)
        order_contains_dish(1,2,1)
        customer_rated_dish(1,1,4)
        customer_rated_dish(1,2,5)

        customer_rated_dish(2,1,5)
        customer_rated_dish(2,2,4)
        customer_rated_dish(2,3,4)

        customer_rated_dish(3,3,5)
        customer_rated_dish(3,4,4)

        customer_rated_dish(4,4,5)
        customer_rated_dish(4,5,5)

        customer_rated_dish(5,5,4)
        customer_rated_dish(5,6,4)

        customer_rated_dish(6,6,4)
        customer_rated_dish(6,7,5)

        customer_rated_dish(7,7,4)
        customer_rated_dish(7,8,5)

        customer_rated_dish(8,8,4)
        customer_rated_dish(8,9,5)

        customer_rated_dish(9, 9, 4)
        customer_rated_dish(9, 10, 5)

        customer_rated_dish(10, 10, 4)
        customer_rated_dish(10, 11, 5)

        customer_rated_dish(11, 5, 5)
        customer_rated_dish(11,12,4)

        customer_rated_dish(12,3,4)
        customer_rated_dish(12,13,5)
        customer_rated_dish(12,16,4)

        customer_rated_dish(13,14,5)

        customer_rated_dish(14,14,4)
        customer_rated_dish(14,15,4)

        customer_rated_dish(15, 1, 5)
        customer_rated_dish(15,2,4)

        customer_rated_dish(16, 17, 5)
        customer_rated_dish(16, 18, 5)
        customer_rated_dish(16, 19, 5)

        c1_recommended_dishes = [
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            16
        ]
        self.assertEqual(c1_recommended_dishes, get_potential_dish_recommendations(1), 'test 17.36')



if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)

# If you fail any assert when running the
# tests all at once - try running them
# individually, as there is quite a lot
# going on here. Also, some tests are named
# after a single function, but actually
# test more than one.

# Test numbers (e.g. 'test 11.35') don't mean
# anything, they're just there to make it
# easy to know which assert failed, and
# they might not be in consecutive or
# correct order.
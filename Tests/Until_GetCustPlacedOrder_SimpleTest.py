import unittest
from datetime import datetime

import Solution as Solution
from Business.Dish import Dish, BadDish
from Business.Order import Order, BadOrder
from Solution import drop_tables
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
        self.assertEqual(Customer(cust_id=2, full_name='2', age=22, phone="0123456789"), Solution.get_customer_that_placed_order(2), 'test 6.19')
        self.assertEqual(Customer(cust_id=3, full_name='3', age=22, phone="0123456789"), Solution.get_customer_that_placed_order(3), 'test 6.20')
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(898989), 'test 6.21')


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)

import unittest
import Solution as Solution
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish
from datetime import datetime

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''


class Test(AbstractTest):
    def test_customer(self) -> None:
        c1 = Customer(1, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        c2 = Customer(2, None, 21, "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), '0123456789')

    def test_order(self) -> None:
        o1 = Order(1, datetime(2024, 12, 3, 17, 15, 30), 20, "Alla Ahbar 13")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'Mehabel Order')
        o2 = Order(2, datetime(2024, 12, 3, 17, 15, 30), 10, "Ara")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o2), 'Bad Name')

    def test_dish(self ):
        d1 = Dish(1, "Mithan", 20, True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'Mithan Habala')
        d2 = Dish(2, "Sufle", -1, True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d2), 'Bad Price')

    def test_placed(self):
        p1 = Dish(1, "Mithan", 20, True)
        o1 = Order(1, datetime(2024, 12, 3, 17, 15, 30), 20, "Alla Ahbar 13")
        c1 = Customer(1, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'Mehabel Order')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(p1), 'Mithan Habala')

        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 1), "Try 1")
        self.assertEqual(c1, Solution.get_customer_that_placed_order(1), "Try 11")
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(2), "Try 12")
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,3), "Try 13")
        self.assertEqual([OrderDish(1, 3, 20)], Solution.get_all_order_items(1), "Try 13")

    def test_order_total_price(self):
        dishes = [Dish(i+1, f'Dish #{i + 1}', 10*(i+1), True) for i in range(10)]
        for d in dishes:
            self.assertEqual(ReturnValue.OK, Solution.add_dish(d), f'Test - Dish Insert Dish #{d.get_dish_id()}')

        orders = [Order(i+1, datetime(2025, 1, (i+1)%30, 12, 12, 12), 5*(i+1), f'Yossi Street {10*i}') for i in range(10)]
        for o in orders:
            self.assertEqual(ReturnValue.OK, Solution.add_order(o), f'Test - Order #{o.get_order_id()}')

        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1, 1, 3), 'Test - Insert 3*(Dish #1) to order #1') # Order #1 total price = 5 + 30
        order_total_price_expected = [35]
        self.assertEqual(order_total_price_expected[0], Solution.get_order_total_price(orders[0].get_order_id()), f'Test - Order #{orders[0].get_order_id()} total price')





# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)

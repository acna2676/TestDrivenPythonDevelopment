import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + "/../../stock_alerter"))
print(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)

# from stock_alerter.stock import Stock  # noqa: E402
from stock import Stock  # noqa: E402


class StockTest(unittest.TestCase):
    def test_price_of_a_new_stock_class_should_be_None(self):
        stock = Stock("GOOG")
        self.assertIsNone(stock.price)

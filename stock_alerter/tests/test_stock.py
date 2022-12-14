# exec command: python -m unittest discover -s ../../stock_alerter -t ../../stock_alerter *プロジェクトルートディレクトリとtestsディレクトリに__init__.pyも必要
# exec cimmand with nose2: nose2  -t ../../stock_alerter --plugin nose2.plugins.layers (--layer-reporter -v)
# exec command: per each modules: python -m unittest discover -s ../../stock_alerter -t ../../stock_alerter tests.test_stock
import collections
import unittest
from datetime import datetime, timedelta

# from nose2.tools import such
# from nose2.tools.params import params
from stock import Stock, StockSignal

# def setup_test():
#     global goog
#     goog = Stock("GOOG")


# def teardown_test():
#     global goog
#     goog = None


# def test_price_of_a_new_stock_class_should_be_None():
#     assert goog.price is None, "Price of a newstock should be None"


# test_price_of_a_new_stock_class_should_be_None.setup = setup_test
# test_price_of_a_new_stock_class_should_be_None.teardown = teardown_test


# def given_a_series_of_prices(stock, prices):
#     timestamps = [datetime(2014, 2, 10), datetime(2014, 2, 11),
#                   datetime(2014, 2, 12), datetime(2014, 2, 13)]
#     for timestamp, price in zip(timestamps, prices):
#         stock.update(timestamp, price)


# @params(
#     ([8, 10, 12], True),
#     ([8, 12, 10], False),
#     ([8, 10, 10], False)
# )
# def test_stock_trends(prices, expected_output):
#     goog = Stock("GOOG")
#     given_a_series_of_prices(goog, prices)
#     assert goog.is_increasing_trend() == expected_output


# def test_trend_with_all_consecutive_values_upto_100():
#     for i in range(100):
#         yield stock_trends_with_consecutive_prices, [i, i+1, i+2]


# def stock_trends_with_consecutive_prices(prices):
#     goog = Stock("GOOG")
#     given_a_series_of_prices(goog, prices)
#     assert goog.is_increasing_trend()


# with such.A("Stock class") as it:

#     @it.has_setup
#     def setup():
#         it.goog = Stock("GOOG")

#     with it.having("a price method"):
#         @it.has_setup
#         def setup():
#             it.goog.update(datetime(2014, 2, 12), price=10)

#         @it.should("return the price")
#         def test(case):
#             assert it.goog.price == 10

#         @it.should("return the latest price")
#         def test(case):
#             it.goog.update(datetime(2014, 2, 11), price=15)
#             assert it.goog.price == 10

#     with it.having("a trend method"):
#         @it.should("return True if the last three updates were increasing")
#         def test(case):
#             it.goog.update(datetime(2014, 2, 11), price=12)
#             it.goog.update(datetime(2014, 2, 12), price=13)
#             it.goog.update(datetime(2014, 2, 13), price=14)
#             assert it.goog.is_increasing_trend()

#     it.createTests(globals())


# class StockTest(unittest.TestCase):
#     def setUp(self):
#         self.goog = Stock("GOOG")

#     def test_price_of_a_new_stock_class_should_be_None(self):
#         self.assertIsNone(self.goog.price)

#     def test_stock_update(self):
#         """An update should set the price on the
#         stock object
#         We will be using the `datetime` module
#         for the timestamp """
#         self.goog.update(datetime(2014, 2, 12), price=10)
#         self.assertEqual(10, self.goog.price)

#     def test_negative_price_should_throw_ValueError(self):
#         with self.assertRaises(ValueError):
#             self.goog.update(datetime(2014, 2, 13), -1)

#     def test_stock_price_should_give_the_latest_price(self):
#         self.goog.update(datetime(2014, 2, 12), price=10)
#         self.goog.update(datetime(2014, 2, 13), price=8.4)
#         self.assertAlmostEqual(8.4, self.goog.price, delta=0.0001)


# class StockTrendTest(unittest.TestCase):


class StockTrendTest(unittest.TestCase):
    def setUp(self):
        self.goog = Stock("GOOG")

    # def given_a_series_of_prices(self, prices):
    #     timestamps = [datetime(2014, 2, 10), datetime(2014, 2, 11), datetime(2014, 2, 12),
    #                   datetime(2014, 2, 13)]
    #     for timestamp, price in zip(timestamps, prices):
    #         self.goog.update(timestamp, price)

    def given_a_series_of_prices(self, stock, prices):
        timestamps = [datetime(2014, 2, 10), datetime(2014, 2, 11),
                      datetime(2014, 2, 12), datetime(2014, 2, 13)]
        for timestamp, price in zip(timestamps, prices):
            stock.update(timestamp, price)

    def test_stock_trends(self):
        dataset = [
            ([8, 10, 12], True),
            ([8, 12, 10], True),
            ([8, 10, 10], True)
        ]
        for data in dataset:
            prices, output = data
            with self.subTest(prices=prices, output=output):
                goog = Stock("GOOG")
                self.given_a_series_of_prices(goog, prices)
                self.assertEqual(output, goog.is_increasing_trend())

    # def test_increasing_trend_is_true_if_price_increase_for_3_updates(self):
    #     self.given_a_series_of_prices([8, 10, 12])
    #     self.assertTrue(self.goog.is_increasing_trend())

    # def test_increasing_trend_is_false_if_price_decreases(self):
    #     self.given_a_series_of_prices([8, 12, 10])
    #     self.assertFalse(self.goog.is_increasing_trend())

    # def test_increasing_trend_is_false_if_price_equal(self):
    #     self.given_a_series_of_prices([8, 10, 10])
    #     self.assertFalse(self.goog.is_increasing_trend())


class StockCrossOverSignalTest(unittest.TestCase):
    def setUp(self):
        self.goog = Stock("GOOG")

    def _flatten(self, timestamps):
        for timestamp in timestamps:
            if not isinstance(timestamp, collections.Iterable):
                yield timestamp
            else:
                for value in self._flatten(timestamp):
                    yield value

    def _generate_timestamp_for_date(self, date, price_list):
        if not isinstance(price_list, collections.Iterable):
            return date
        else:
            delta = 1.0/len(price_list)
            return [date + i*timedelta(delta) for i in range(len(price_list))]

    def _generate_timestamps(self, price_list):
        return list(self._flatten([self._generate_timestamp_for_date(datetime(2014, 2, 13) - timedelta(i), price_list[len(price_list)-i-1]) for i in range(len(price_list) - 1, -1, -1) if price_list[len(price_list) - i - 1] is not None]))

    def given_a_series_of_prices(self, price_list):
        timestamps = self._generate_timestamps(price_list)
        for timestamp, price in zip(timestamps, list(self._flatten([p for p in price_list if p is not None]))):
            self.goog.update(timestamp, price)

    def test_generate_timestamp_returns_consecutive_dates(self):
        price_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        expected = [
            datetime(2014, 2, 3), datetime(2014, 2, 4), datetime(2014, 2, 5),
            datetime(2014, 2, 6), datetime(2014, 2, 7), datetime(2014, 2, 8),
            datetime(2014, 2, 9), datetime(2014, 2, 10), datetime(2014, 2, 11),
            datetime(2014, 2, 12), datetime(2014, 2, 13)]
        self.assertEqual(expected, self._generate_timestamps(price_list))

    def test_generate_timestamp_skips_empty_dates(self):
        price_list = [1, 2, 3, None, 5, 6, 7, 8, 9, 10, 11]
        expected = [
            datetime(2014, 2, 3), datetime(2014, 2, 4), datetime(2014, 2, 5),
            datetime(2014, 2, 7), datetime(2014, 2, 8),
            datetime(2014, 2, 9), datetime(2014, 2, 10), datetime(2014, 2, 11),
            datetime(2014, 2, 12), datetime(2014, 2, 13)]
        self.assertEqual(expected, self._generate_timestamps(price_list))

    def test_generate_timestamp_handles_multiple_updates_per_date(self):
        price_list = [1, 2, 3, [4, 3], 5, 6, 7, 8, 9, 10, 11]
        expected = [
            datetime(2014, 2, 3), datetime(2014, 2, 4), datetime(2014, 2, 5),
            datetime(2014, 2, 6), datetime(2014, 2, 6, 12),
            datetime(2014, 2, 7), datetime(2014, 2, 8),
            datetime(2014, 2, 9), datetime(2014, 2, 10), datetime(2014, 2, 11),
            datetime(2014, 2, 12), datetime(2014, 2, 13)]
        self.assertEqual(expected, self._generate_timestamps(price_list))

    def test_stock_with_no_data_returns_neutral(self):
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([])
        self.assertEqual(StockSignal.neutral,
                         self.goog.get_crossover_signal(date_to_check))

    def test_stock_with_less_data_returns_neutral(self):
        """Even though the series has a downward crossover, we return neutral
        because there are not enough data points"""
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            20, 21, 22, 23, 24, 25, 26, 27, 28, 1])
        self.assertEqual(StockSignal.neutral,
                         self.goog.get_crossover_signal(date_to_check))

    def test_stock_with_no_crossover_returns_neutral(self):
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEqual(StockSignal.neutral,
                         self.goog.get_crossover_signal(date_to_check))

    def test_with_downward_crossover_returns_sell(self):
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 4])
        self.assertEqual(StockSignal.sell,
                         self.goog.get_crossover_signal(date_to_check))

    def test_with_upward_crossover_returns_buy(self):
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 46])
        self.assertEqual(StockSignal.buy,
                         self.goog.get_crossover_signal(date_to_check))

    def test_should_only_look_at_closing_price(self):
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            29, [5, 28], [5, 27], 26, 25, 24, 23, 22, 21, 20, [5, 46]])
        self.assertEqual(StockSignal.buy,
                         self.goog.get_crossover_signal(date_to_check))

    def test_should_be_neutral_if_not_enough_days_of_data(self):
        """Even though we have 13 updates, they only cover 10 days"""
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            [5, 28], [5, 27], 26, 25, 24, 23, 22, 21, 20, [5, 46]])
        self.assertEqual(StockSignal.neutral,
                         self.goog.get_crossover_signal(date_to_check))

    def test_should_pick_up_previous_closing_if_no_updates_for_a_day(self):
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            29, 28, 27, 26, 25, 24, 23, 22, 21, 20, None, None, 46])
        self.assertEqual(StockSignal.buy,
                         self.goog.get_crossover_signal(date_to_check))

    def test_should_have_11_days_worth_of_data(self):
        """Should return signal even if there is less than 11 number of updates
        as in the case where some days have no updates but we pick up the
        previous closing price to fill in the value"""
        date_to_check = datetime(2014, 2, 13)
        self.given_a_series_of_prices([
            27, 26, 25, 24, 23, 22, 21, 20, None, None, 46])
        self.assertEqual(StockSignal.buy,
                         self.goog.get_crossover_signal(date_to_check))

    def test_date_to_check_can_be_beyond_last_update_date(self):
        """We have updates upto 13th, but we are checking signal on 15th.
        It should just fill in the values for 14th and 15th since there are
        no updates on these days"""
        date_to_check = datetime(2014, 2, 15)
        self.given_a_series_of_prices([
            29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 46])
        self.assertEqual(StockSignal.neutral,
                         self.goog.get_crossover_signal(date_to_check))

import unittest
from datetime import datetime
from unittest import mock

from alert import Alert
from event import Event
from rule import PriceRule
from stock import Stock


class TestAction:
    executed = False

    def execute(self, description):
        self.executed = True


class AlertTest(unittest.TestCase):
    # def test_action_is_executed_when_rule_matches(self):
    #     exchange = {"GOOG": Stock("GOOG")}
    #     rule = PriceRule("GOOG", lambda stock:
    #                      stock.price > 10)
    #     action = TestAction()
    #     alert = Alert("sample alert", rule,
    #                   action)
    #     alert.connect(exchange)
    #     exchange["GOOG"].update(datetime(2014, 2, 10), 11)
    #     self.assertTrue(action.executed)

    # def test_action_is_executed_when_rule_matches(self):
    #     exchange = {"GOOG": Stock("GOOG")}
    #     rule = PriceRule("GOOG", lambda stock: stock.price > 10)
    #     action = mock.MagicMock()
    #     alert = Alert("sample alert", rule, action)
    #     alert.connect(exchange)
    #     exchange["GOOG"].update(datetime(2014, 2, 10), 11)
    #     action.execute.assert_called_with("sample alert")

    # def test_action_is_executed_when_rule_matches(self):
    #     exchange = {"GOOG": Stock("GOOG")}
    #     rule = mock.MagicMock(spec=PriceRule)
    #     rule.matches.return_value = True
    #     rule.depends_on.return_value = {"GOOG"}
    #     action = mock.MagicMock()
    #     alert = Alert("sample alert", rule, action)
    #     alert.connect(exchange)
    #     exchange["GOOG"].update(datetime(2014, 2, 10), 11)
    #     action.execute.assert_called_with("sample alert")

    def test_action_is_executed_when_rule_matches(self):
        goog = mock.MagicMock(spec=Stock)
        goog.updated = Event()
        goog.update.side_effect = lambda date, value: goog.updated.fire(self)
        exchange = {"GOOG": goog}
        rule = mock.MagicMock(spec=PriceRule)
        rule.matches.return_value = True
        rule.depends_on.return_value = {"GOOG"}
        action = mock.MagicMock()
        alert = Alert("sample alert", rule, action)
        alert.connect(exchange)
        exchange["GOOG"].update(datetime(2014, 2, 10), 11)
        action.execute.assert_called_with("sample alert")

import unittest
from unittest import mock

from event import Event


class Mock:
    def __init__(self):

        self.called = False
        self.params = ()

    def __call__(self, *args, **kwargs):

        self.called = True
        self.params = (args, kwargs)


class EventTest(unittest.TestCase):

    # def test_a_listener_is_notified_when_an_event_is_raised(self):
    #     listener = Mock()
    #     event = Event()
    #     event.connect(listener)
    #     event.fire()
    #     self.assertTrue(listener.called)

    def test_a_listener_is_notified_when_an_event_is_raised(self):
        listener = mock.Mock()
        event = Event()
        event.connect(listener)
        event.fire()
        self.assertTrue(listener.called)

    def test_a_listener_is_passed_right_parameters(self):
        listener = mock.Mock()
        event = Event()
        event.connect(listener)
        event.fire(5, shape="square")
        # self.assertEquals(((5, ), {"shape": "square"}), listener.params)
        listener.assert_called_with(5, shape="square")

    def test_a_listener_is_passed_right_parameters(self):
        listener = mock.Mock()
        event = Event()
        event.connect(listener)
        event.fire(5, shape="square")
        listener.assert_has_calls([mock.call(5, shape="square")])

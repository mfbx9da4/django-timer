# -*- coding: utf-8 -*-
import mock

from django_timer import Timer
from unittest import TestCase


@mock.patch('django_timer.log.info')
class TimerTest(TestCase):
    def test_caller(self, logger_mock):
        with Timer() as timer:
            pass
        self.assertEqual(timer.caller, 'django_timer.test.test_caller:11 :: ')

    def test_no_message(self, logger_mock):
        with Timer() as timer:
            pass
        parts = timer.__str__().split('::')
        self.assertEqual(len(parts), 2)

    def test_decorator(self, logger_mock):
        @Timer('asdf')
        def fn():
            pass
        fn()
        self.assertEqual(logger_mock.call_count, 1)

    def test_delta(self, logger_mock):
        with mock.patch('time.time', side_effect=[0.0, 10.0]):
            with Timer() as timer:
                pass
            self.assertEqual(timer.delta, 10.0)

    def test_average(self, logger_mock):
        with mock.patch('time.time', side_effect=[2.0, 4.0, 6.0, 8.0, 10.0, 12.0]):
            with Timer() as timer:
                for x in xrange(4):
                    timer.lap()
            self.assertEqual(timer.delta, 10.0)
            self.assertEqual(timer.average, 2.0)
            self.assertEqual(logger_mock.call_count, 0)

    def test_average_zero_laps(self, logger_mock):
        with mock.patch('time.time', side_effect=[2.0, 4.0, 6.0]):
            with Timer() as timer:
                for x in xrange(0):
                    timer.lap()
            self.assertEqual(timer.averagePretty(), '0 laps')
            self.assertEqual(logger_mock.call_count, 0)

# -*- coding: utf-8 -*-
import datetime

import mock

from django import test

from .. import models
from .. import main
from .. import exceptions
from .. import settings
from ..decorators import confirm_action


@confirm_action
def simple_action(param_first, param_second):
    return {'status': 'done'}


@confirm_action
def error_during_process():
    raise exceptions.ErrorDuringProcess


@confirm_action
def system_fault():
    raise Exception

@confirm_action
def wrong_data_return():
    return 42


class SetActionTestCase(test.TestCase):

    def test_wrong_path(self):
        with self.assertRaises(exceptions.NotActionException):
            main.set_action('+7911', 'asdfsadf', {})

    def test_wrong_module(self):
        with self.assertRaises(exceptions.NotActionException):
            main.set_action('+7911', 'asdf.asdfsadf', {})

    def test_wrong_func(self):
        with self.assertRaises(exceptions.NotActionException):
            main.set_action('+7911', 'sys.asdfsadf', {})

    def test_wrong_function(self):
        with self.assertRaises(exceptions.NotActionException):
            main.set_action('+7911', 'inspect.isfunction', {})

    def test_all_ok(self):
        action = main.set_action(
            '+7911',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 4
            }
        )
        self.assertIsNotNone(action.pk)

    def test_live_time(self):
        action = main.set_action(
            '+7911',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 4
            },
            live_time=15
        )
        self.assertEquals(action.live_time, 15)

    def test_generation_func(self):
        gen_func = lambda: '2048'

        action = main.set_action(
            '+7911',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 4
            },
            generate_code_func=gen_func
        )
        self.assertEquals(action.confirm_code, '2048')

    def test_send_func(self):
        class TestException(Exception):
            pass

        def send_func(user_contact, message):
            raise TestException

        with self.assertRaises(exceptions.DidNotSendMessage):
            main.set_action(
                '+7911',
                'confirmaction.tests.test_main.simple_action',
                {
                    'param_first': 'test',
                    'param_second': 4
                },
                send_code_func=send_func
            )


class ApplyActionTestCase(test.TestCase):

    def test_wrong_code(self):
        action = main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 'param'
            }
        )

        with self.assertRaises(exceptions.WrongCode):
            main.apply_action(action.pk, '3482332')

    def test_used_code(self):
        gen_func = lambda: '2048'
        action = main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 'param'
            },
            generate_code_func=gen_func
        )

        main.apply_action(action.pk, '2048')

        with self.assertRaises(exceptions.UsedAction):
            main.apply_action(action.pk, '2048')

    def test_out_of_date(self):
        gen_func = lambda: '2048'

        action = main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 'param'
            },
            generate_code_func=gen_func,
            send_code_func=lambda *args: True
        )

        with mock.patch('confirmaction.models.Action.is_actual') as mock_meth:
            mock_meth.return_value = False
            with self.assertRaises(exceptions.OutOfDate):
                main.apply_action(action.pk, '2048')

    def test_action_done(self):
        gen_func = lambda: '2048'
        action = main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.simple_action',
            {
                'param_first': 'test',
                'param_second': 'param'
            },
            generate_code_func=gen_func
        )

        status, data = main.apply_action(action.pk, '2048')

        self.assertIn('status', data)

        self.assertEquals(status, models.Action.FINISHED_SUCCESS)

    def test_action_error_during_process(self):
        gen_func = lambda: '2048'
        action = main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.error_during_process',
            generate_code_func=gen_func
        )

        status, data = main.apply_action(action.pk, '2048')

        self.assertIn('error', data)
        self.assertEquals(status, models.Action.ERROR_DURING_PROCESS)

    def test_action_system_fault(self):
        gen_func = lambda: '2048'
        action = main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.system_fault',
            generate_code_func=gen_func
        )

        status, data = main.apply_action(action.pk, '2048')

        self.assertIn('error', data)
        self.assertEquals(status, models.Action.ACTION_FAULT)

    def test_action_wrong_data_returned(self):
        gen_func = lambda: '2048'
        action = main.set_action(
            '+8952342343',
            'confirmaction.tests.test_main.wrong_data_return',
            generate_code_func=gen_func
        )

        status, data = main.apply_action(action.pk, '2048')

        self.assertIn('error', data)
        self.assertEquals(status, models.Action.WRONG_RETURNED_DATA)

    def test_cant_find_action(self):
        main.set_action(
            'zap@land.ru',
            'confirmaction.tests.test_main.simple_action',
        )

        with self.assertRaises(exceptions.CantFindAction):
            main.apply_action(4096, '2048')

    def test_wrong_code_generator(self):
        original = settings.CONFIRM_GENERATION
        settings.CONFIRM_GENERATION = 'asdfasdf.asdf'
        with self.assertRaises(ValueError):
            main.set_action(
                'zap@land.ru',
                'confirmaction.tests.test_main.simple_action'
            )
        settings.CONFIRM_GENERATION = original

    def test_wrong_send_method(self):
        original = settings.CONFIRM_SEND_METHOD
        settings.CONFIRM_SEND_METHOD= 'asdfasdf.asdf'
        with self.assertRaises(ValueError):
            main.set_action(
                '+79625213997',
                'confirmaction.tests.test_main.simple_action'
            )
        settings.CONFIRM_SEND_METHOD = original


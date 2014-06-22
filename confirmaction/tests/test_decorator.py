# -*- coding: utf-8 -*-
from django import test

from ..decorators import confirm_action


class TestSettingDecorator(test.TestCase):

    def test_set_decorator(self):

        @confirm_action
        def check_function():
            return

        self.assertTrue(hasattr(check_function, 'confirm_action'))
        self.assertTrue(check_function)

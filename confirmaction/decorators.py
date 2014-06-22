# -*- coding: utf-8 -*-
import inspect


def confirm_action(func):
    """
    Set
    """
    assert inspect.isfunction(func), "Func should be function"
    setattr(func, 'confirm_action', True)
    return func
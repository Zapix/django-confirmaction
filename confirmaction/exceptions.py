# -*- coding: utf-8 -*-


class NotActionException(Exception):
    """
    Error raises when passed function not an action.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class CantFindAction(Exception):
    """
    Error raises when can't find action with specia identifier
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Cant find action with identifier %d " % self.value


class WrongDataReturn(Exception):
    """
    Error raises when return data of function not dict
    """
    def __str__(self):
        return "Action should return only dict"


class OutOfDate(Exception):
    """
    Raise exception when tries to start old action
    """
    def __str__(self):
        return "Action out of date"


class WrongCode(Exception):
    """
    Raises exception when somebody used wrong code
    """
    def __str__(self):
        return "Wrong code"


class UsedAction(Exception):
    """
    Raises exception when somebody tries to apply wrong code
    """


class ErrorDuringProcess(Exception):
    # TODO: add value
    """
    Error raised in action if something goes wrong in action.

    Example:
    try:
        User.objects.get(pk=12)
    except User.DoesNotExist:
        raise ErrorDuringProcess("There is no user with pk 12")
    """


class DidNotSendMessage(Exception):
    """
    Error raises when passed function not an action.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


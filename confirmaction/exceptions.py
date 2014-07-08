# -*- coding: utf-8 -*-


class BaseConfirmActionException(Exception):
    """
    Base class for all exceptions raised in django-confirmaction
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class OnCreateActionError(BaseConfirmActionException):
    """
    Exception raises before action set
    """
    pass


class NotActionException(OnCreateActionError):
    """
    Error raises when passed function not an action.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class DidNotSendMessage(OnCreateActionError):
    """
    Error raises when can't send action for some reasons.
    """


class OnConfirmActionError(BaseConfirmActionException):
    """
    Base class for errors raises when confirm action
    """


class ValidateActionError(OnConfirmActionError):
    """
    Base class for errors raises when validate action and code
    """


class CantFindAction(ValidateActionError):
    """
    Error raises when can't find action by path
    """
    pass


class OutOfDate(ValidateActionError):
    """
    Raise exception when tries to start old action
    """


class WrongCode(ValidateActionError):
    """
    Raises exception when somebody used wrong code
    """


class UsedAction(ValidateActionError):
    """
    Raises exception when somebody tries to apply wrong code
    """


class WrongScopeException(ValidateActionError):
    """
    Error raises when use tries to use wrong scope for action
    """


class ProcessActionError(OnConfirmActionError):
    """
    Raises when happened error during process action
    """


class WrongDataReturned(ProcessActionError):
    """
    Error raises when return data of function not dict
    """


class ErrorDuringProcess(ProcessActionError):
    """
    Error raised in action if something goes wrong in action.

    Example:
    try:
        User.objects.get(pk=12)
    except User.DoesNotExist:
        raise ErrorDuringProcess("There is no user with pk 12")
    """


class SystemFaultError(ProcessActionError):
    """
    Raises when catches some error during process action
    """

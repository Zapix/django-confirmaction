# -*- coding: utf-8 -*-
import json
from Crypto.Hash import SHA256

from django.template.loader import render_to_string
from django.utils.importlib import import_module
from django.conf import settings

from . import models
from . import settings as app_settings
from . import exceptions


def _import_func(func_addr):
    if not '.' in func_addr:
        raise ValueError(
            "'%s' is not a func address" % func_addr
        )

    try:
        module = import_module('.'.join(
            func_addr.split('.')[:-1]
        ))
    except ImportError:
        raise ValueError('Can`t find function %s' % func_addr)
    try:
        func = getattr(module, func_addr.split('.')[-1])
    except AttributeError:
        raise ValueError('Can`t find function %s' % func_addr)
    return func


def get_action_func(func_addr):
    try:
        func = _import_func(func_addr)
    except ValueError as e:
        raise exceptions.NotActionException(str(e))

    if not hasattr(func, 'confirm_action') or not func.confirm_action:
        raise exceptions.NotActionException(
            "%s not an action" % func_addr
        )

    return func


def set_action(user_contact, func_addr, func_kwargs=None, scope=None,
               message_template=None, template_context=None, live_time=None,
               generate_code_func=None, send_code_func=None):
    """
    Sets an action. Checks that func_addr - is string with address of function
    and this function is confirm_method action else
    raises :exception:`confirmaction.exceptions.NotActionException`
    checks that all func_kwargs keys, and values are string. else raises
    `confirmaction.exceptions.WrongParamsException`.
    Sets live time from live_time param or settings.LIVE_TIME_CODE,
    Generates_code from generate_code_func or from settings.CONFIRM_GENERATION
    Generates message with message_template or with settings.CONFIRM_MESSAGE_TEMPLATE and
    template_context with action or {}
    Sends code to user_contact via send_code_func or from settings.CONFIRM_SEND_METHOD
    :param user_contact: user contact for sending activation code
    :type user_contact: string
    :param func_addr: address of action function
    :type func_addr: basestring
    :param func_kwargs: - dictionary of params. Keys and values are strings
    :type func_kwargs: - dict
    :param live_time: live time of action could be None
    :type live_time: int
    :param generate_code_func: function for generation code could be None
    :type generate_code_func: function
    :param send_code_func: function for sending code could be None
    :type send_code_func: function
    :returns: action object
    :rtype: :class:`confirmaction.models.Action`
    """
    # TODO: return integer not action
    # TODO: add encription  for code and identifier

    get_action_func(func_addr)

    if func_kwargs is None:
        func_kwargs = {}

    if generate_code_func is None:
        generate_code_func = _import_func(app_settings.CONFIRM_GENERATION)

    code = generate_code_func()

    action = models.Action.objects.create(
        user_contact=user_contact,
        action_func=func_addr,
        scope=scope,
        code_hash=SHA256.new(settings.SECRET_KEY + code).hexdigest(),
        live_time=live_time or app_settings.CODE_LIVE_TIME
    )

    models.ActionArg.objects.bulk_create(
        [
            models.ActionArg(action=action, name=key, value=value)
            for key, value in func_kwargs.iteritems()
        ]
    )

    if send_code_func is None:
        send_code_func = _import_func(app_settings.CONFIRM_SEND_METHOD)

    message_template = (
        message_template or app_settings.ACTIVATION_MESSAGE_TEMPLATE
    )

    template_context = template_context or {}
    template_context.update({'code': code})

    try:
        send_code_func(
            user_contact,
            render_to_string(message_template, template_context)
        )
    except Exception as e:
        action.delete()
        raise exceptions.DidNotSendMessage(str(e))

    return action.pk


def apply_action(action_pk, code, scope=None):
    """
    Applies action if code is correct and not out of date and is opened
    If it is out of date raise OutOfDate exception.
    If code is wrong raise WrongCode exception
    If code isn't opened raise UsedAction
    If all ok return status confirmaction.models.Action.FINISHED_SUCCESS and
    dict with result
    If something goes wrong return error status and message of error
    """
    try:
        action = models.Action.objects.get(pk=action_pk)
    except models.Action.DoesNotExist:
        raise exceptions.CantFindAction(
            "Can't find action with pk %d" % action_pk
        )

    if (
        action.scope is None and not scope is None or
        not action.scope is None and scope is None or
        not action.scope is None and not scope is None and action.scope != scope
    ):
        raise exceptions.WrongScopeException(
            "%s is a wrong scope" % (action.scope or "Default")
        )

    if not action.is_actual():
        raise exceptions.OutOfDate("Action is out of date")

    code_hash = SHA256.new(settings.SECRET_KEY + code).hexdigest()
    if not action.code_hash == code_hash:
        raise exceptions.WrongCode("Wrong code")

    if action.action_status != models.Action.NOT_CONFIRMED:
        raise exceptions.UsedAction("Used action")

    func = get_action_func(action.action_func)
    try:
        data = func(**action.get_kwargs())
    except (exceptions.ErrorDuringProcess, Exception) as e:
        action.result = str(e)
        if isinstance(e, exceptions.ErrorDuringProcess):
            raise exceptions.ErrorDuringProcess(str(e))
        else:
            action.action_status = models.Action.ACTION_FAULT
            action.save()
            raise exceptions.SystemFaultError(str(e))
    else:
        if not isinstance(data, dict):
            action.action_status = models.Action.WRONG_RETURNED_DATA
            action.save()
            raise exceptions.WrongDataReturned(
                "Action should return serializable dict"
            )
        try:
            action.result = json.dumps(data)
        except ValueError:
            action.action_status = models.Action.WRONG_RETURNED_DATA
            action.save()
            raise exceptions.WrongDataReturned(
                "Action should return serializable dict"
            )
        action.action_status = models.Action.FINISHED_SUCCESS
        action.save()

    return data


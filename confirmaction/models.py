# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from . import settings as app_settings


class Action(models.Model):
    """
    Model for action
    """
    OUT_OF_DATE = -1
    OPENED = 0
    CONFIRMED = 1

    CODE_STATUSES = (
        (OUT_OF_DATE, _("Out of date")),
        (OPENED, _("Opened")),
        (CONFIRMED, _("Confirmed"))
    )

    NOT_CONFIRMED = 0
    FINISHED_SUCCESS = 1
    WRONG_RETURNED_DATA = -1
    ERROR_DURING_PROCESS = -2
    ACTION_FAULT = -3

    ACTION_STATUS = (
        (NOT_CONFIRMED, _("Not confirmed")),
        (FINISHED_SUCCESS, _("Finished success")),
        (WRONG_RETURNED_DATA, _("Wrong returned data")),
        (ERROR_DURING_PROCESS, _('Error during process')),
        (ACTION_FAULT, _('Action fault'))
    )

    user_contact = models.CharField(
        verbose_name=_("User contact"),
        max_length=255
    )
    action_func = models.CharField(
        verbose_name=_("Action function"),
        max_length=255,
    )
    confirm_code = models.CharField(
        verbose_name=_("Confirm code"),
        max_length=255
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name=_("Updated"),
        auto_now=True
    )
    executed = models.DateTimeField(
        verbose_name=_("Executed"),
        blank=True,
        null=True
    )
    action_status = models.IntegerField(
        verbose_name=_("Action status"),
        choices=ACTION_STATUS,
        default=NOT_CONFIRMED
    )
    result = models.TextField(
        verbose_name=_("Result"),
        blank=True,
        null=True
    )
    live_time = models.IntegerField(
        verbose_name=_("Live time"),
        blank=True,
        null=True
    )

    def is_actual(self):
        return timezone.now() < self.created + datetime.timedelta(
            minutes=self.live_time or app_settings.CODE_LIVE_TIME
        )

    def get_kwargs(self):
        return {x.name:x.value for x in self.arg_set.all()}


class ActionArg(models.Model):
    """
    Model for saving params of action
    """
    action = models.ForeignKey(
        'Action',
        related_name='arg_set'
    )
    name = models.CharField(
        _("Argument name"),
        max_length=255
    )
    value = models.CharField(
        _("Argument value"),
        max_length=255
    )

    class Meta:
        verbose_name = _("Action argument")
        verbose_name_plural = _("Action arguments")
# -*- coding: utf-8 -*-
from django.conf import settings


CONFIRM_GENERATION = getattr(
    settings,
    'CONFIRM_GENERATION',
    'confirmaction.utils.generate_code'
)

CONFIRM_SEND_METHOD = getattr(
    settings,
    'CONFIRM_SEND_METHOD',
    'confirmaction.utils.send_code'
)

CODE_LIVE_TIME = getattr(
    settings,
    'CODE_LIVE_TIME',
    60
)

ACTIVATION_MESSAGE_TEMPLATE = getattr(
    settings,
    'ACTIVATION_MESSAGE_TEMPLATE',
    'confirmaction/activation_message.html'
)
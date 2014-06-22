# -*- coding: utf-8 -*-
import logging
import random

from django.conf import settings

logger = logging.getLogger('django')


def generate_code():
    """
    Default function for generating confirmation code
    """
    return ''.join(str(random.randint(0,9)) for x in range(4))


def send_code(user_contact, message):
    """
    Sends message to user. Works only in debug mode. In production mode should
    be implemented
    :param user_contact: email/phone etc for sending message to user
    :type user_contact: basestring
    :param message: message with activation code for user
    :type message: basestring
    """
    logger.critical(
        "Should be implemented in production and set in CONFIRM_SEND_METHOD"
    )
    logger.debug("Contact: %s" % user_contact)
    logger.debug(message)

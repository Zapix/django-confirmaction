# -*- coding: utf-8 -*-
import logging
import random

logger = logging.getLogger('confirmaction')


def generate_code():
    """
    Default function for generating confirmation code
    """
    return ''.join(str(random.randint(0,9)) for x in range(4))


def log_send_code(user_contact, message):
    """
    Print message into log
    :param user_contact: email/phone etc for sending message to user
    :type user_contact: basestring
    :param message: message with activation code for user
    :type message: basestring
    """
    logger.debug(
        "Should be implemented in production and set in CONFIRM_SEND_METHOD"
    )
    logger.debug("Contact: %s" % user_contact)
    logger.debug(message)

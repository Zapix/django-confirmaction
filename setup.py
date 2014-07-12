# -*- coding: utf-8 -*-
import os
from setuptools import setup

LONG_DESCRIPTION = """
Django confirmaction is a battery for confirm actions via email, sms etc.
"""


def long_description():
    try:
        return open(
            os.path.join(os.path.dirname(__file__), "README.md")
        ).read()
    except IOError:
        return LONG_DESCRIPTION

setup(
    name = "django-confirmaction",
    version = "0.0.3",
    author = "Aleksandr Aibulatov",
    author_email = "zap.aibulatov@gmail.com",
    description = "Django battery for confirm some action via email, sms, etc",
    license = "BSD",
    keywords = "django, battery, confirm action",
    url = "https://github.com/Zapix/django-confirmaction",
    packages=[
        'confirmaction',
        'confirmaction.migrations'
    ],
    long_description=long_description(),
    install_requires=[
        'django>=1.6',
        'south>=0.8.4',
        'pycrypto'
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
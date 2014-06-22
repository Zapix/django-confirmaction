# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-confirmaction",
    version = "0.0.1",
    author = "Aleksandr Aibulatov",
    author_email = "zap.aibulatov@gmail.com",
    description = "Django battery for confirm some action via email, sms, etc",
    license = "BSD",
    keywords = "django, battery, confirm action",
    url = "https://github.com/Zapix/django-confirmaction",
    packages=[
        'confirmaction',
        'confirmaction.tests',
        'confirmaction.migrations'
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
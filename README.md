====================
django-confirmaction
====================

[![Build Status](https://travis-ci.org/Zapix/django-confirmaction.png?branch=master)](https://travis-ci.org/Zapix/django-confirmaction)

Django module for confirm actions via sending email/sms or etc.

------------
Installation
------------

You can install via PyPi_ or direct from the github_ repo.

To install with pip::

    $ pip install django-choices

-----------
Basic usage
-----------

1. To start working please add this module in INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'confirmaction',
        ...
    )

2. Create a function for sending activation code. Function should have 2 parameters
user_contact, and message. For example in module `myapp.sending` create function for send message::

    def send_message(user_contact, message):
        print "Contact:", user_contact
        print "Message:", message

3. Set sending function on settings.py::

    CONFIRM_SEND_METHOD = 'myapp.sending.send_message'

4. Create an action. Action it is a function decorated with `confirm_action`.
Function can have string parameters, and should return dict which can json-serializable
For example create action in module myapp.actions::

    from confirmcation import confirm_action

    @confirm_action
    activate_user(user_pk):
        user = User.objects.get(pk=user_pk)
        user.is_active = True
        user.save()
        return {
            'status': 'activated',
            'user_pk': user_pk
        }

5. Create a view where code will be send. For sending code use `confirmaction.set_action`::

    from confirmaction import set_action

    def register_user(request):
        # register user
        ...
        action_pk = set_action(
            user.email,
            'myapp.actions.activate_user',
            'user_pk': user.pk
        )
        ...

6. Create a view where action will be confirm::

    from confirmaction import apply_action

    def confirm_action(request):
        code = request.POST.get('code')
        action_pk = request.POST.get('action_pk')

        result = apply_action(action_pk, code)

        #handle result
        .....

7. Use it :)

# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .. import exceptions
from ..main import set_action
from ..decorators import confirm_action


User = get_user_model()

@confirm_action
def activate_user_phone(user_pk):
    user = User.objects.get(pk=user_pk)
    user.is_active = True
    user.save()
    return {'message': 'User is active'}



@confirm_action
def system_fault():
    raise Exception


class ConfirmActionTestCase(APITestCase):

    def test_wrong_code(self):
        action_pk = set_action(
            'zap@land.ru',
            'confirmaction.tests.test_view.activate_user_phone',
            {'user_pk': 12}
        )
        response = self.client.post(
            reverse('confirm-action', kwargs={'pk': action_pk}),
            {'code': '14811485'}
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_function_fault(self):
        action_pk = set_action(
            '+79625213997',
            'confirmaction.tests.test_view.system_fault',
            generate_code_func=lambda: '2048'
        )
        response = self.client.post(
            reverse('confirm-action', kwargs={'pk': action_pk}),
            {'code': '2048'},
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_all_ok(self):
        user = User.objects.create(
            username='test',
            email='test@test.ru',
            password='test',
            is_active=False
        )
        action_pk = set_action(
            user.email,
            'confirmaction.tests.test_view.activate_user_phone',
            {'user_pk': user.pk},
            generate_code_func=lambda: '2048'
        )

        response = self.client.post(
            reverse('confirm-action', kwargs={'pk': action_pk}),
            {'code': '2048'}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.is_active)

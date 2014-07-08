from rest_framework import status
from rest_framework import response
from rest_framework.views import APIView

from . import exceptions
from .main import apply_action
from .models import Action


class ConfirmCodeView(APIView):

    def post(self, request, pk, *args, **kwargs):

        try:
            data = apply_action(pk,
                                request.DATA.get('code', ''))
        except exceptions.OnConfirmActionError as e:
            http_status = status.HTTP_400_BAD_REQUEST
            data = {'error': unicode(e)}
        else:
            http_status = status.HTTP_200_OK

        return response.Response(data, status=http_status)

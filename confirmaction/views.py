from rest_framework import status
from rest_framework import response
from rest_framework.views import APIView

from . import exceptions
from .main import apply_action
from .models import Action


class ConfirmCodeView(APIView):

    def post(self, request, pk, *args, **kwargs):

        try:
            action_status, data = apply_action(pk,
                                               request.DATA.get('code', ''))
        except exceptions.CantFindAction as e:
            http_status = status.HTTP_400_BAD_REQUEST
            data = {'error': unicode(e)}
        except exceptions.UsedAction as e:
            http_status = status.HTTP_400_BAD_REQUEST
            data = {'error': unicode(e)}
        except exceptions.OutOfDate as e:
            http_status = status.HTTP_400_BAD_REQUEST
            data = {'error': unicode(e)}
        except exceptions.WrongCode as e:
            http_status = status.HTTP_400_BAD_REQUEST
            data = {'error': unicode(e)}
        else:
            if action_status == Action.FINISHED_SUCCESS:
                http_status = status.HTTP_200_OK
            else:
                http_status = status.HTTP_400_BAD_REQUEST

        return response.Response(data, status=http_status)

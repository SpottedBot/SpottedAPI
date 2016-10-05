from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datasets.models import Spam, NotSpam
from datasets.serializers import SpamSerializer, NotSpamSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.throttling import ScopedRateThrottle
from datasets.models import NotEval, Spam, NotSpam
import json

# Create your views here.


# spam-list/
class SpamList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'list'

    def get(self, request):
        spam = Spam.objects.all()
        serializer = SpamSerializer(spam, many=True)
        response = {
            'count': len(serializer.data),
            'data': serializer.data
        }
        return Response(response)


# not-spam-list/
class NotSpamList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'list'

    def get(self, request):
        spam = NotSpam.objects.all()
        serializer = NotSpamSerializer(spam, many=True)
        response = {
            'count': len(serializer.data),
            'data': serializer.data
        }
        return Response(response)


class EvalMessage(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'eval'

    def post(self, request):
        content = {
            'message': request.POST['message'],
            'user': request.user,
        }

        # eval message
        eval = False

        # add message to noteval
        e = NotEval(message=content['message'], spam=eval, user=content['user'])
        e.save()

        response = {
            'isSpam': eval,
        }
        return Response(response)


class SubmitData(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAdminUser,)

    def post(self, request):
        content = {
            'list': request.POST['list'],
        }
        spam = 0
        n_spam = 0
        try:
            for element in json.loads(content['list']):
                if element['spam']:
                    spam += 1
                    s = Spam(message=element['message'])
                    s.save()
                else:
                    n_spam += 1
                    s = NotSpam(message=element['message'])
                    s.save()
        except:
            return Response({'status': 'unsuccessful',
                             'spam_add': spam,
                             'not_spam_add': n_spam})

        return Response({'status': 'successful',
                         'spam_add': spam,
                         'not_spam_add': n_spam})

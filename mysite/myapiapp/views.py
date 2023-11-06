from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from shopapp.models import Product, Order
from .serializers import UserSerializer, GroupSerializer


class OncePerMinuteUserThrottle(UserRateThrottle):
    rate = '1/min'


@api_view(["GET"])
@throttle_classes([OncePerMinuteUserThrottle])
def hello_view(request: Request) -> Response:
    return Response({"message": "Hello for now! See you after a one minutes!"})


class GroupsListView(ListModelMixin, GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)


class UsersListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

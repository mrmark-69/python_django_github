from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .serializers import UserSerializer

class OncePerHourUserThrottle(UserRateThrottle):
    rate = '1/min'


@api_view(["GET"])
@throttle_classes([OncePerHourUserThrottle])
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello for now! See you after a one minutes!"})


class GroupsListView(APIView):
    def get(self, request: Request) -> Response:
        data = [group.name for group in Group.objects.all()]
        return Response({"groups": data})


class UsersListView(APIView):
    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        return Response({"users": serialized.data})

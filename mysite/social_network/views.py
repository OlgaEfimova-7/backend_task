from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from social_network.models import User
from social_network.serializers import UserSerializer
from social_network.helpers import shortest_path_search

from collections import deque


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Users accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def get_friends(self, request, pk=None):
        """Endpoint returns user friends by user id"""
        user = User.objects.filter(id=pk).first()
        if user:
            friends = user.friends.all()
            serializer = self.get_serializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"status": f"User with user_id:{pk} not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False)
    def get_shorter_connection(self, request):
        """Endpoint returns the list of ids, which represents the shortest connections path
         between two specified users. If users are directly connected, empty list will be given"""
        start_profile_id = int(request.query_params.get("start_id"))
        end_profile_id = int(request.query_params.get("end_id"))

        check_entitnes = User.objects.filter(id__in=[start_profile_id, end_profile_id])
        if check_entitnes.count() != 2:
            return Response(
                {"status": f"Users entities not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ids_list = shortest_path_search(start_profile_id, end_profile_id)

        if not isinstance(ids_list, list):
            return Response(
                {
                    "status": f"The shortest path doesn't exist. The specified users are not linked"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(ids_list, status=status.HTTP_200_OK)

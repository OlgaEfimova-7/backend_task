from django.test import TestCase
from social_network import helpers
from social_network.models import User, FriendList
from unittest.mock import patch


def fake_get_friends_ids(current_vertex):
    """Fake function, that simulates the work with DB 
    and returns the list of connected ids"""
    return HelperTestCase.graph.get(current_vertex)


class HelperTestCase(TestCase):
    """Class contains tests for functions, implemented in helpers.py file"""

    fixtures = ["social_network/tests/users_data.json"]
    # The following structure represens oriented unweighted graph.
    # The key is a number of graph's vertex, value list - vertexes, connected to the current vertex
    # For example, "1" vertex is connected to  "2" and "3" vertexes
    graph = {1: [2, 3], 2: [5], 3: [4], 4: [5, 6], 5: [], 6: []}

    def test_get_friends_ids(self):
        """Ensure we can get the queryset of user friends by id"""
        users = User.objects.all().order_by("id")
        first_user = users[0]
        second_user = users[1]
        FriendList.objects.create(profile=first_user, friend=second_user)

        self.assertQuerySetEqual(
            User.objects.filter(id=first_user.id)
            .first()
            .friends.values_list("id", flat=True),
            helpers.get_friends_ids(first_user.id),
        )
        self.assertQuerySetEqual([], helpers.get_friends_ids(second_user.id))

    def test_get_list_of_ids(self):
        """Check the logic of restorind the ids order, based on the parents relationships"""
        parent_list = {6: 4, 5: 2, 4: 3, 3: 1, 2: 1}
        self.assertEqual([2], helpers.get_list_of_ids(1, 5, parent_list))
        self.assertEqual([], helpers.get_list_of_ids(1, 3, parent_list))
        self.assertEqual([3], helpers.get_list_of_ids(1, 4, parent_list))
        self.assertEqual([3, 4], helpers.get_list_of_ids(1, 6, parent_list))

    @patch("social_network.helpers.get_friends_ids", fake_get_friends_ids)
    def test_shortest_path_search(self):
        """Check the logic of the shortest path searching"""
        self.assertEqual([2], helpers.shortest_path_search(1, 5))
        self.assertEqual([3, 4], helpers.shortest_path_search(1, 6))
        self.assertEqual(None, helpers.shortest_path_search(5, 1))
        self.assertEqual([], helpers.shortest_path_search(1, 2))

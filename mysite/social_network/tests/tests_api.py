from copy import deepcopy
from rest_framework import status
from rest_framework.test import APITestCase
from social_network.models import User, FriendList
from django.forms.models import model_to_dict


class UserTests(APITestCase):
    fixtures = ["social_network/tests/users_data.json"]
    users_data = [
        {
            "img": "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
            "first_name": "Steph",
            "last_name": "Walters",
            "phone": "(820) 289-1818",
            "address": "5190 Center Court Drive",
            "city": "Spring",
            "state": "TX",
            "zipcode": "77370",
            "available": True,
        },
        {
            "img": "https://randomuser.me/api/portraits/med/men/67.jpg",
            "first_name": "Arnoldo",
            "last_name": "Almonte",
            "phone": "(684) 873 2299",
            "address": "9400, Calzada Carrero",
            "city": "San Miguel El Alto",
            "state": "Puebla",
            "zipcode": "97706",
            "available": True,
        },
    ]

    def setUp(self):
        """Friends connections setup"""
        users = User.objects.all().order_by("id")
        FriendList.objects.create(profile=users[0], friend=users[1])

    def test_create_user_profile(self):
        """Ensure we can create a new user object."""
        users_existed = User.objects.all().count()
        for data in self.users_data:
            response = self.client.post("/users/", data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2 + users_existed)

    def test_get_users_list(self):
        """Ensure we can get the list of users"""
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user_profile_by_id(self):
        """Ensure we can get user by id"""
        db_user = User.objects.all().first()
        response = self.client.get(f"/users/{db_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_db_user = model_to_dict(db_user)
        friends_ids = [friend.id for friend in expected_db_user.get("friends")]
        expected_db_user["friends"] = friends_ids
        self.assertEqual(response.data, expected_db_user)

    def test_update_user_profile(self):
        """Ensure we can update user by id"""
        user_id = User.objects.all().first().id
        updated_data = deepcopy(self.users_data[0])
        updated_data["first_name"] = "Ana"
        updated_data["last_name"] = "Lindner"

        response = self.client.put(f"/users/{user_id}/", updated_data, format="json")
        updated_user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            model_to_dict(updated_user)["first_name"], updated_data["first_name"]
        )
        self.assertEqual(
            model_to_dict(updated_user)["last_name"], updated_data["last_name"]
        )

    def test_get_friends(self):
        """Ensure we can get user friends by user id"""
        # check success status
        db_user = User.objects.all().order_by("id").first()
        response = self.client.get(f"/users/{db_user.id}/get_friends/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            model_to_dict(friend) for friend in model_to_dict(db_user).get("friends")
        ]
        self.assertEqual(response.data, expected_data)

        # check failed status (for a non-existent user)
        db_user_ids = User.objects.all().values_list("id", flat=True)
        response = self.client.get(f"/users/{max(db_user_ids)+1}/get_friends/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_shorter_connection(self):
        """Ensure we can get the shortest connection between two specified users"""
        db_user_ids = User.objects.all().order_by("id").values_list("id", flat=True)
        # check success status
        response = self.client.get(
            f"/users/get_shorter_connection/?start_id={db_user_ids[0]}&end_id={db_user_ids[1]}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # check failed status (for a non-existent user)
        response = self.client.get(
            f"/users/get_shorter_connection/?start_id={max(db_user_ids)+1}&end_id={max(db_user_ids)+2}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_users(self):
        """Ensure we can delete users by id"""
        users = User.objects.all()
        for user in users:
            response = self.client.delete(f"/users/{user.id}/")
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

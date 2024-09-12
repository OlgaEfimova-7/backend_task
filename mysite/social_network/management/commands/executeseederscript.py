from django.core.management.base import BaseCommand
import random
from social_network.models import User, FriendList
import requests


class Command(BaseCommand):
    help = "Execute the seeder script."

    def add_arguments(self, parser):
        parser.add_argument(
            "--profilesTotal",
            help="Total number of user profiles, that should be created in database",
            required=True,
            type=int,
        )
        parser.add_argument(
            "--friendsTotal",
            help="Total number of friends connections, that should be randomly created",
            required=True,
            type=int,
        )

    def handle(self, *args, **options):
        """Seeder script execution"""
        profilesTotal = options["profilesTotal"]
        friendsTotal = options["friendsTotal"]

        # Check, if it is necessary to create additional profiles,
        # based on the number of already created profiles in DB
        created_profiles = User.objects.all()
        created_profiles_num = created_profiles.count()
        # If profilesTotal <= existed DB users, new profiles won't be created
        self.stdout.write("Checking, if additional user profiles creation is necessary")
        if profilesTotal > created_profiles_num:
            self.stdout.write(f"{profilesTotal - created_profiles_num} additional users should be created")
            self.generate_additional_users(profilesTotal - created_profiles_num)
        else:
            self.stdout.write(
                f"User profiles creation is not necessary. Number of user profiles in DB - {created_profiles_num}"
            )

        # Random generation of friends connections
        self.stdout.write(f"Starting to generate random friends connection")
        user_profiles = User.objects.all().order_by("id")
        result_list = []
        for _ in range(friendsTotal):
            random_user = random.randint(1, user_profiles.count())
            random_friend = random.randint(1, user_profiles.count())
            # to avoid self connection
            while random_user == random_friend:
                random_friend = random.randint(1, user_profiles.count())
            friend_connection = FriendList(
                profile=user_profiles[random_user - 1],
                friend=user_profiles[random_friend - 1],
            )
            result_list.append(friend_connection)
        FriendList.objects.bulk_create(result_list)
        self.stdout.write(f"Friends connections created")


    def generate_additional_users(self, num: int):
        """Method generates the specified number of random users profiles,
        using https://randomuser.me/api/"""
        self.stdout.write(f"Starting to create {num} user profiles")
        result_list = []
        for _ in range(num):
            r = requests.get("https://randomuser.me/api/")
            random_user_data = r.json()
            user = User(
                img=random_user_data["results"][0]["picture"]["medium"],
                first_name=random_user_data["results"][0]["name"]["first"],
                last_name=random_user_data["results"][0]["name"]["last"],
                phone=random_user_data["results"][0]["phone"],
                address=f'{random_user_data["results"][0]["location"]["street"]["number"]}, '
                f'{random_user_data["results"][0]["location"]["street"]["name"]}',
                city=random_user_data["results"][0]["location"]["city"],
                state=random_user_data["results"][0]["location"]["state"],
                zipcode=random_user_data["results"][0]["location"]["postcode"],
                available=True,
            )
            result_list.append(user)
        User.objects.bulk_create(result_list)
        self.stdout.write(f"User profiles created")

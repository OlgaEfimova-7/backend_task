from django.test import TestCase
from django.core.management import call_command
from social_network.models import User, FriendList


class SeederScriptTestCase(TestCase):
    def test_executeseederscript(self):
        "Test executeseederscript command."

        args = []
        opts = {"profilesTotal": 5, "friendsTotal": 5}
        call_command("executeseederscript", *args, **opts)
        self.assertEqual(5, User.objects.all().count())
        self.assertEqual(5, FriendList.objects.all().count())

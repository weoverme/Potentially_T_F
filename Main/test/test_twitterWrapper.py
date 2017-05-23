import unittest

from Main.twitterWrapper import TwitterWrapper


class TestTwitterWrapper(unittest.TestCase):

    def setUp(self):
        self.valid_tw = TwitterWrapper("@realDonaldTrump", 1)
        self.invalid_tw = TwitterWrapper("@baracomaba", 1)

    def test_init_valid(self):
        self.assertEqual(self.valid_user, self.valid_tw.username, "Username is incorrect")

    def test_init_invalid(self):
        self.assertEqual("", self.invalid_tw.username)

    def test_get_tweets_for_pos_int(self):
        pass


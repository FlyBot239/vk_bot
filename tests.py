import unittest
import vk_api
from functions import get_friends, list_of_mutual_friends, make_connection


class Test(unittest.TestCase):
    example = 279760424
    guys = ['312653751', '279760424']

    # paste your token
    token = ""

    def setUp(self):
        self.connection = vk_api.VkApi(token=self.token)

    def test_make_connection(self):
        x = make_connection(self.token)
        self.assertEqual(self.token, x.token['access_token'])

    def test_get_friends(self):
        x = get_friends(self.connection, self.example)
        self.assertIsInstance(x, set)

    def test_list_of_mutual_friends(self):
        x = list_of_mutual_friends(self.connection, self.guys)
        self.assertIsInstance(x, list)


if __name__ == "__main__":
    unittest.main()

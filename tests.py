import unittest
import vk_api
from bot import get_friends, list_of_mutual_friends, make_connection


class Test(unittest.TestCase):
    def setUp(self):
        file = open('info_for_test.txt')
        text = file.read().split('\n')
        file.close()
        self.token = text[0].split(':')[1].strip()
        self.example = int(text[1].split(':')[1])
        self.guys = list(map(int, text[2].split(':')[1].split(',')))
        self.connection = vk_api.VkApi(token=self.token)

    def test_make_connection(self):
        x = make_connection(self.token)
        self.assertEqual(self.token, x.token['access_token'])

    def test_get_friends(self):
        x = get_friends(self.connection, self.example)
        self.assertIsInstance(x, set)

    def test_list_of_mutual_friends(self):
        x = list_of_mutual_friends(self.connection, list(map(str, self.guys)))
        self.assertIsInstance(x, list)


if __name__ == "__main__":
    unittest.main()

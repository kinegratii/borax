# codng=utf8


import unittest

from borax.datasets import join_one


class shortcutMethodTestCase(unittest.TestCase):
    def test_join_one(self):
        data_list = [
            {"id": 1, "name": ""},
            {"id": 2, "name": ""},
            {"id": 4, "name": ""},
        ]
        values = {1: "A", 2: "B"}
        join_one(data_list, values, from_="id", as_="name")
        self.assertEqual("A", data_list[0]["name"])
        self.assertEqual("", data_list[2]["name"])

    def test_join_one_choices(self):
        data_list = [
            {"id": 1, "name": "Amy", "gender": 1},
            {"id": 2, "name": "John", "gender": 2},
        ]
        gender_choices = [(1, "male"), (2, "female")]

        join_one(data_list, gender_choices, from_="gender", as_="gender_name")
        self.assertEqual("male", data_list[0]["gender_name"])

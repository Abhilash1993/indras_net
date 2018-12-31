"""
This is the test suite for entity.py.
"""

import json

from unittest import TestCase, main

from entity import Entity, NAME_ID, SEP

leibbyear = 1646
leibdyear = 1716

def create_leibniz():
    name = "Leibniz"
    attrs = {"place": 0.0, "time": leibbyear}
    return Entity(name, attrs)

def create_other_leibniz():
    name = "Leibniz"
    attrs = {"place": 1.0, "time": leibbyear}
    return Entity(name, attrs)

def create_newton():
    name = "Newton"
    attrs = {"place": 0.0, "time": 1658.0, "achieve": 43.9}
    return Entity(name, attrs)

class EntityTestCase(TestCase):
    def test_eq(self):
        l1 = create_leibniz()
        l2 = create_leibniz()
        l3 = create_other_leibniz()
        n = create_newton()
        self.assertEqual(l1, l2)
        self.assertNotEqual(l1, n)
        self.assertNotEqual(l1, l3)
        # add a field and see that they aren't equal:
        l2["derivatives"] = 1.0
        self.assertNotEqual(l1, l2)

    def test_str(self):
        name = "Ramanujan"
        ent = Entity(name)
        self.assertEqual(name, str(ent))

    def test_repr(self):
        name = "Hardy"
        age_nm = "age"
        age = 141.0
        attrs = {age_nm: age}
        ent = Entity(name, attrs)
        rep = '{"name": "Hardy", "attrs": {"age": 141.0}}'
        self.assertEqual(rep, repr(ent))

    def test_len(self):
        ent = create_newton()
        self.assertEqual(len(ent), 3)

    def test_get(self):
        ent = create_leibniz()
        self.assertEqual(ent["time"], leibbyear)

    def test_set(self):
        ent = create_leibniz()
        ent["time"] = leibdyear
        self.assertEqual(ent["time"], leibdyear)

    def test_contains(self):
        ent = create_leibniz()
        s = "place"
        self.assertTrue(s in ent)

    def test_enttype(self):
        l1 = create_leibniz()
        l2 = create_other_leibniz()
        n = create_newton()
        self.assertTrue(l1.same_type(l2))
        self.assertFalse(l1.same_type(n))

if __name__ == '__main__':
    main()
